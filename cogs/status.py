from asyncio import wait_for
from discord.ext import commands, bridge
from discord.ext.bridge import Bot
from discord import Embed, utils as dutils
from utils import Utils

class Status(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["s"], description="Get the server status")
    async def status(self, ctx, serverip=None):
        if serverip is None:
            cursor = await Utils.mysql_login()
            database = cursor.cursor()
            database.execute("SELECT server_ip FROM server WHERE guild_id = %s", [ctx.guild.id])
            try:
                result = database.fetchone()[0]
            except TypeError:
                database.close()
                cursor.close()
                return await Utils.respond(ctx, "Sorry, but this server does not have an IP registered. Please use `setserver` for that.")
            serverip = result
            database.close()
            cursor.close()
        if not serverip.endswith(".aternos.me"):
            serverip += ".aternos.me"
        if serverip.count(".") > 2:
            return await Utils.respond(ctx, "Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        if serverip.count(":") == 1:
            if len(serverip.split(":")[1]) != 5:
                return await Utils.respond(ctx, "Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        await ctx.defer()
        try:
            stat = await wait_for(Utils.get_server_status(serverip), timeout=3)
        except TimeoutError:
            return await Utils.respond(ctx, "Uh oh! The protocol took too long to respond! This will likely fix itself.")
        embed = Embed(title=serverip)
        if stat.version.name == "§4● Offline":
            embed.description = "We are not able to gather info from offline servers, sorry!\nProtocol Latency: " + str(
                round(
                    stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Utils.Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        elif stat.version.name == "⚠ Error":
            embed.description = "Server does not exist\nProtocol Latency: " + str(round(
                stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Utils.Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        elif stat.version.name == "§4● Starting":
            embed.description = "We are not able to gather info from starting servers, sorry!\nProtocol Latency: " + str(
                round(
                    stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Utils.Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        else:
            embed.add_field(name="**__Status__**", value="Online", inline=True)
            embed.add_field(name="**__Players__**", value=str(stat.players.online) + "/" + str(stat.players.max),
                            inline=True)
            embed.add_field(name="**__Software__**", value=stat.version.name, inline=True)
            embed.add_field(name="**__MOTD__**", value=Utils.remove_colors_from_string(stat.description), inline=False)
            embed.colour = Utils.Colors.green
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        await Utils.respond(ctx, embed=embed)


def setup(bot: Bot):
    bot.add_cog(Status(bot))
