import socket
import builtins
from discord import Intents, Status, Activity, ActivityType, Bot

from config.directories import Directories
from providers.modifiers.logger import setup_logger
from database.executioners.initiator import db_pool
from providers.database.migration_provider import run_migrations
from providers.database.seeding_provider import run_seeders
from providers.translation.get_translate import Translation

from config.app import Settings

logger = setup_logger()


intents = Intents(guilds=True)
bot = Bot(
    intents=intents,
    status=Status.online,
    activity=Activity(
        type=ActivityType.playing,
        name="starting up script..."))


def check_hostname():
    production_hostname = Settings().get_hostname()
    current_hostname = socket.gethostname()
    return production_hostname == current_hostname


def setup_settings():
    settings = Settings()
    token = settings.get_token()
    seeding = settings.get_setting('seeding')
    environment = settings.get_environment()
    manager_guilds = settings.get_setting('manager_guilds')
    return token, seeding, environment, manager_guilds


async def main():
    token, seeding, environment, manager_guilds = setup_settings()  # pylint: disable=unused-variable
    if check_hostname() and environment != 'production':
        logger.warning(
            'Environment was set to "{}" on a production machine and has been set to "production".'.format(environment))
        Settings().set_environment('production')
    if environment not in ('testing', 'development'):
        logger.warning(
            'Environment was set to "{}" on a non-production machine and has been set to "development".'.format(environment))
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
    module_directory = Directories().get_directory('modules')
    bot.load_extensions(module_directory, recursive=True)
    if setup_settings()[2] == 'development':
        await bot.sync_commands(guild_ids=setup_settings()[-1])
    logger.info(f'{bot.user} has connected to Discord successfully.')


@bot.listen()
async def on_ready():
    builtins.t = Translation().t
    await bot.change_presence(status=Status.online, activity=Activity(type=ActivityType.listening, name="interactions"))
    logger.info(f'{bot.user} has been logged into successfully.')


@bot.listen()
async def on_disconnect():
    logger.warning('Bot has disconnected from discord. Shutting down pool...')
    await db_pool.close_pool()
    logger.info('Pool has been closed successfully.')
    logger.info(f'{bot.user} has disconnected from Discord successfully.')


bot.run(setup_settings()[0])
