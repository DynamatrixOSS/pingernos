from discord.ext import commands
from discord import Embed, utils as dutils
from mcstatus import JavaServer
from utils.utils import Utils
class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx, serverip = None):
        if serverip is None:
            return await ctx.reply("Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        if not serverip.endswith(".aternos.me"):
            return await ctx.reply("Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        if serverip.count(".") > 2:
            return await ctx.reply("Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        async with ctx.typing():
            server = await JavaServer.async_lookup(serverip)
            stat = await server.async_status()
            embed = Embed(title=serverip)
            #Check if the motd is §4● Offline
            if stat.version.name == "§4● Offline":
                embed.description = "We are not able to gather info from offline servers, sorry!\nProtocol Latency: " + str(round(stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
                embed.colour = Utils.Colors.red
                embed.timestamp = dutils.utcnow()
                embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
            elif stat.version.name == "⚠ Error":
                embed.description = "Server does not exist\nProtocol Latency: " + str(round(stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
                embed.colour = Utils.Colors.red
                embed.timestamp = dutils.utcnow()
                embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
            else:
                embed.add_field(name="**__Status__**", value="Online", inline=True)
                embed.add_field(name="**__Players__**", value=str(stat.players.online) + "/" + str(stat.players.max), inline=True)
                embed.add_field(name="**__Software__**", value=stat.version.name, inline=True)
                embed.add_field(name="**__MOTD__**", value=Utils.removeColorsFromString(stat.description), inline=False)
                embed.color = Utils.Colors.green
                embed.timestamp = dutils.utcnow()
                embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
            await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))
