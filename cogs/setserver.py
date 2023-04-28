from discord.ext import commands, bridge
from utils import Utils

class SetServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_manage_guild_permission(self, ctx): #Credits to the google AI BARD for generating this code, i don't know why py-cord's built in method didn't work=
        author = ctx.author

        # Get the author's guild permissions
        permissions = author.guild_permissions

        # Check if the author has the manage guild permission
        return permissions.manage_guild

    @bridge.bridge_command(aliases=["set"],
                           description="Set the default server to use if no argument is provided in the status command.")
    async def setserver(self, ctx, server=None):
        if not self.has_manage_guild_permission(ctx):
            return await ctx.respond("You need the `Manage Server` permission to use this command.")
        if server is None:
            return await ctx.respond(
                "Please provide a server IP to register to this guild. If an IP is already registered, it'll be overwritten")
        if not server.endswith(".aternos.me"):
            server += ".aternos.me"
        if server.count(".") > 2:
            return await ctx.respond("Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        cursor = await Utils.mysql_login()
        database = cursor.cursor()
        database.execute(
            "INSERT INTO server (guild_id, server_ip) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_ip = %s",
            (ctx.guild_id, server, server))
        cursor.commit()
        database.close()
        cursor.close()
        await ctx.respond(f'The IP has been set to {server}. Use `status` without an argument to view it.')

def setup(bot):
    bot.add_cog(SetServer(bot))
