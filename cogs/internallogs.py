import aiohttp
from discord.ext import commands
from discord import Guild, Embed, Webhook
from discord.ext.bridge import Bot
from utilities.database import mysql_login
from utilities.data import Colors, get_data


class InternalLogs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        cursor = await mysql_login()
        database = cursor.cursor()
        database.execute("SELECT * FROM blacklist WHERE guild_id = %s", [guild.id])

        try:
            result = database.fetchone()[0]
            print(f'Guild {guild} attempted to add {self.bot.user.name}, but was blacklisted.')
            embed = Embed(title="Joined a guild!", color=Colors.red)
            embed.add_field(name="Name", value=guild.name, inline=True)
            embed.add_field(name="ID", value=guild.id, inline=True)
            embed.description(f'Guild attempted to add {self.bot.user.name}, but is blacklisted:\n**{result["reason"]}**')
            embed.set_thumbnail(url=guild.icon.url)
            async with aiohttp.ClientSession() as client_session:
                webhook = Webhook.from_url(get_data()['Logs']["JoinWebhook"], session=client_session)
                await webhook.send(embed=embed, username="Pingernos Logs", avatar_url=self.bot.user.avatar.url)
            await guild.leave()
        except TypeError:
            pass

        embed = Embed(title="Joined a guild!", color=Colors.green)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(get_data()['Logs']["JoinWebhook"], session=client_session)
            await webhook.send(embed=embed, username="Pingernos Logs", avatar_url=self.bot.user.avatar.url)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        embed = Embed(title="Left a guild!", color=Colors.red)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(get_data()['Logs']["LeaveWebhook"], session=client_session)
            await webhook.send(embed=embed, username="Pingernos Logs", avatar_url=self.bot.user.avatar.url)

def setup(bot: Bot):
    bot.add_cog(InternalLogs(bot))
