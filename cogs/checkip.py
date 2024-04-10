from asyncio import wait_for

import discord
from discord import slash_command, option, Embed

from utilities.data import Colors, get_server_status
from utilities.utility import check_ip


class CheckIP(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(aliases=["checkserverip", "check"], description="Checks if an Aternos-IP is free to use.")
    @option("address", str, description="The Aternos-IP to check")
    async def checkip(self, ctx, address):
        address = check_ip(address)
        if not address:
            return await ctx.respond("Please provide a valid Aternos IP.", ephemeral=True)
        nip = address.split(".")[0]
        if len(nip) > 20 or len(nip) < 4:
            return await ctx.respond(f"Aternos IPs must contain between 4 to 20 characters. You have {len(nip)}/20 characters.", ephemeral=True)
        await ctx.defer()
        embed = Embed()
        stat = await wait_for(get_server_status(address), timeout=2)
        if stat.version.name == "⚠ Error":
            embed.description = f"**{address}** is free to use!\nTo use it as your server address, head to **[the options of your server](https://aternos.org/options)**"
            embed.colour = Colors.green
        else:
            embed.description = f"**{address}** is already taken!"
            embed.colour = Colors.red
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(CheckIP(bot))
