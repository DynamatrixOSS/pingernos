from discord.ext import commands, bridge
from discord.ext.bridge import Bot
from utils import Utils

class SetServer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["set"],
                           description="Set the default server to use if no argument is provided in the status command.")
    @bridge.has_permissions(manage_guild=True)
    async def setserver(self, ctx, server=None):
        if server is None:
            return await Utils.respond(ctx,
                "Please provide a server IP to register to this guild. If an IP is already registered, it'll be overwritten")
        if not server.endswith(".aternos.me"):
            server += ".aternos.me"
        if server.count(".") > 2:
            return await Utils.respond(ctx, "Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        cursor = await Utils.mysql_login()
        database = cursor.cursor()
        database.execute(
            "INSERT INTO server (guild_id, server_ip) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_ip = %s",
            (ctx.guild_id, server, server))
        cursor.commit()
        database.close()
        cursor.close()
        await Utils.respond(ctx, f'The IP has been set to {server}. Use `status` without an argument to view it.')

def setup(bot: bridge.Bot):
    bot.add_cog(SetServer(bot))
