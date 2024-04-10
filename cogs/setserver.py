import discord
from discord import slash_command
from discord.ext import commands

from utilities.database import modifier
from utilities.utility import check_ip


class SetServer(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    @commands.has_permissions(manage_guild=True)
    async def setserver(self, ctx, server=None):
        """ Set the default server to use if no argument is provided in the status command """
        if server is None:
            await modifier("DELETE FROM server WHERE guild_id = %s", [ctx.guild_id])
            return await ctx.respond("Default server has been removed. Use `setserver <server>` to set a new one.", ephemeral=True)
        server = check_ip(server)
        if not server:
            return await ctx.respond("Please provide a valid Aternos IP.", ephemeral=True)

        await modifier("INSERT INTO server (guild_id, server_ip) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_ip = %s", [ctx.guild_id, server, server])
        await ctx.respond(f'The IP has been set to {server}. Use `status` without an argument to view it.' , ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(SetServer(bot))
