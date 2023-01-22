from discord.ext import commands
from discord import Embed
from utils.data.utils import utils
import re
from mcstatus import JavaServer
class CheckIP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["checkserverip", "check"], description = "Checks if an Aternos-IP is free to use.")
    async def checkip(self, ctx, ip):
        if ip is None:
            return await ctx.reply("Please provide a Aternos server ip!\nExample: example.aternos.me")
        if not re.match(r"^(\w+)(?:\.aternos\.me)?$", ip):
            return await ctx.reply(f"`{ip}`is not a valid Aternos server IP or name.")
        if ip.count(".") > 2:
            return await ctx.reply("Please provide a valid Aternos server ip!\nExample: example.aternos.me")
        nip = ip.split(".")[0]
        if len(nip) > 20:
            return await ctx.reply("Aternos IPs can only be 20 characters long, please try a shorter one. Yours is " + str(len(nip)) + " characters long.")
        if len(nip) < 4:
            return await ctx.reply("Aternos IPs must be at least 4 characters long, please try a longer one. Yours is " + str(len(nip)) + " characters long.")
        async with ctx.typing():
            embed = Embed()
            server = await JavaServer.async_lookup(ip)
            stat = await server.async_status()
            if stat.version.name == "⚠ Error":
                embed.description=f"**{nip}.aternos.me** is free to use!\nTo use it as your server address, head to **[the options of your server](https://aternos.org/options)**"
                embed.colour = utils.colors.green
            else:
                embed.description=f"**{nip}.aternos.me** is already taken!"
                embed.colour = utils.colors.red
            await ctx.reply (embed=embed)


def setup(bot):
    bot.add_cog(CheckIP(bot))