import discord
from discord import slash_command, option
from discord.ext import commands
from discord.ext.bridge import Bot
from utils import Utils


class Blacklist(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    @commands.is_owner()
    @option("server", discord.Guild, description="The server to blacklist")
    @option("reason", str, description="The reason for the blacklist")
    async def blacklist(self, ctx, server, reason):
        """ Blacklist a server from the bot """
        cursor = await Utils.mysql_login()
        database = cursor.cursor()
        database.execute("INSERT IGNORE INTO blacklist (guild_id, reason) VALUES (%s, %s)", (server.id, reason))
        cursor.commit()
        database.close()
        cursor.close()
        return await ctx.respond(f'Successfully added guild {server} to the blacklist for:\n**{reason}**')


def setup(bot: Bot):
    bot.add_cog(Blacklist(bot))
