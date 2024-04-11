import aiohttp
import discord
from discord import Guild, Embed, Webhook
from discord.ext import commands

from utilities.data import Colors, get_data
from utilities.database import selector


class InternalLogs(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        result = await selector("SELECT * FROM blacklist WHERE guild_id = %s", [guild.id])

        if result:
            await guild.leave()

        embed = Embed(title="Joined a guild!", color=Colors.green)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        if result:
            embed.description = f'**THIS GUILD IS BLACKLISTED**\n**Reason:** {result[1]}'
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(get_data()['Logs']["JoinWebhook"], session=client_session)
            await webhook.send(embed=embed, username="Pingernos Logs", avatar_url=self.bot.user.avatar.url)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        result = await selector("SELECT * FROM blacklist WHERE guild_id = %s", [guild.id])
        embed = Embed(title="Left a guild!", color=Colors.red)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Guild member count", value=guild.member_count, inline=True)
        embed.add_field(name="Current server count", value=len(self.bot.guilds), inline=True)
        if result:
            embed.description = f'**THIS GUILD IS BLACKLISTED**\n**Reason:** {result[1]}'
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon)
        async with aiohttp.ClientSession() as client_session:
            webhook = Webhook.from_url(get_data()['Logs']["LeaveWebhook"], session=client_session)
            await webhook.send(embed=embed, username="Pingernos Logs", avatar_url=self.bot.user.avatar.url)


def setup(bot: discord.Bot):
    bot.add_cog(InternalLogs(bot))
