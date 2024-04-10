import discord
from discord import slash_command, option
from discord.ext import commands

from utilities.database import modifier
from utilities.utility import check_ip


class SetServer(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    @commands.has_permissions(manage_guild=True)
    @option("server", description="The server to set as default", default=None)
    async def setserver(self, ctx, server):
        """ Set the default server to use if no argument is provided in the status command """
        if not server:
            await modifier("DELETE FROM server WHERE guild_id = %s", [ctx.guild_id])
            return await ctx.respond(f"Default server has been removed. Use </{ctx.command.name}:{ctx.command.id}> with the \"server\" option to set a new one.", ephemeral=True)
        server = check_ip(server)
        if not server:
            return await ctx.respond("Please provide a valid Aternos IP.", ephemeral=True)
        await modifier("INSERT INTO server (guild_id, server_ip) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_ip = %s", [ctx.guild_id, server, server])
        status_command = self.bot.get_application_command("status")
        await ctx.respond(f'The IP has been set to {server}. Use </{status_command.name}:{status_command.id}> without an argument to view it.', ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(SetServer(bot))
