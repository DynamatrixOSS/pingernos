from discord.ext import commands, bridge
from discord.ext.bridge import Bot
from utilities.database import modifier


class SetServer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["set"], description="Set the default server to use if no argument is provided in the status command.")
    @bridge.has_permissions(manage_guild=True)
    async def setserver(self, ctx, server=None):
        if server is None:
            await modifier("DELETE FROM server WHERE guild_id = %s", [ctx.guild_id])
            return await ctx.respond("Default server has been removed. Use `setserver <server>` to set a new one.")
        if not server.endswith(".aternos.me"):
            server += ".aternos.me"
        if server.count(".") > 2:
            return await ctx.respond("Please provide a valid Aternos server ip!\nExample: example.aternos.me")

        await modifier("INSERT INTO server (guild_id, server_ip) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_ip = %s", [ctx.guild_id, server, server])
        await ctx.respond(f'The IP has been set to {server}. Use `status` without an argument to view it.')


def setup(bot: bridge.Bot):
    bot.add_cog(SetServer(bot))
