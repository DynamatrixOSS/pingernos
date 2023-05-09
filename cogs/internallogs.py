import aiohttp
from discord.ext import commands
from discord import Guild, Embed, Webhook
from discord.ext.bridge import Bot
from utils import Utils

class InteralLogs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        embed = Embed(title="Joined a guild!", color=Utils.Colors.green)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(Utils.get_data()['Logs']["JoinWebhook"], session=client_session)
            await webhook.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        embed = Embed(title="Left a guild!", color=Utils.Colors.red)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(Utils.get_data()['Logs']["LeaveWebhook"], session=client_session)
            await webhook.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(InteralLogs(bot))
