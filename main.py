import asyncio
import atexit
import socket
from datetime import datetime
from providers.modifiers.logger import setup_logger
from database.executioners.initiator import db_pool

import discord
import json
from discord import Intents, Status, Activity, ActivityType
from providers.database.migration_provider import run_migrations
from providers.database.seeding_provider import run_seeders

from config.app import Settings

logger = setup_logger()


intents = Intents(guilds=True)
bot = discord.Bot(intents=intents, status=Status.online,
                  activity=Activity(type=ActivityType.playing, name="starting up script..."))


def check_hostname():
    production_hostname = Settings().get_hostname()
    current_hostname = socket.gethostname()
    return production_hostname == current_hostname


def setup_settings():
    token = Settings.get_token()
    seeding = Settings().get_setting('seeding')
    environment = Settings().get_environment()
    return token, seeding, environment


async def main():
    token, seeding, environment = setup_settings()
    if check_hostname() and environment != 'production':
        logger.warning('Environment was set to "{}" on a production machine and has been set to "production".'.format(environment))
        Settings().set_environment('production')
    if environment != 'testing' and environment != 'development':
        logger.warning('Environment was set to "{}" on a non-production machine and has been set to "development".'.format(environment))
        Settings().set_environment('development')

    migrations = False if environment != 'development' else Settings().get_setting('migrations')

    if migrations:
        logger.info('Running migrations...')
        await run_migrations()
        logger.info('Finished migrations.')
    if seeding:
        logger.info('Running seeders...')
        await run_seeders()
        logger.info('Finished seeders.')
    else:
        logger.info('There were no providers to run.')


@bot.listen()
async def on_connect():
    logger.info('Creating pool and connecting to pool...')
    await db_pool.init_pool()
    logger.info('Running providers...')
    await main()
    logger.info(f'{bot.user} has connected to Discord successfully.')


@bot.listen()
async def on_ready():
    # bot.load_extensions("modules")
    await bot.change_presence(status=Status.online, activity=Activity(type=ActivityType.listening, name="interactions"))
    logger.info(f'{bot.user} has been logged into successfully.')


@bot.listen()
async def on_disconnect():
    logger.warning('Bot has disconnected from discord. Shutting down pool...')
    await db_pool.close_pool()
    logger.info('Pool has been closed successfully.')
    logger.info(f'{bot.user} has disconnected from Discord successfully.')

atexit.register(lambda: asyncio.run(db_pool.close_pool()))

bot.run(setup_settings()[0])
