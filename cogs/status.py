from asyncio import wait_for

import discord
from discord import slash_command, option, Embed, utils as dutils

from utilities.data import remove_colors_from_string, Colors, get_server_status
from utilities.database import selector
from utilities.utility import check_ip


class Status(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    @option("serverip", str, description="The Aternos-IP to check", default=None)
    async def status(self, ctx, serverip):
        """ Get the server status """
        if not serverip:
            serverip = (await selector('SELECT server_ip FROM server WHERE guild_id = %s', [ctx.guild.id]))[0]
            if not serverip:
                setserver_command = self.bot.get_application_command("setserver")
                return await ctx.respond(f"Sorry, but this server does not have an IP registered. Please use </{setserver_command.name}:{setserver_command.id}> for that.", ephemeral=True)
        serverip = check_ip(serverip)
        if not serverip:
            return await ctx.respond("Please provide a valid Aternos IP.", ephemeral=True)
        await ctx.defer()
        try:
            stat = await wait_for(get_server_status(serverip), timeout=3)
        except TimeoutError:
            return await ctx.respond("Uh oh! The protocol took too long to respond! This will likely fix itself.", ephemeral=True)
        embed = Embed(title=serverip)
        if stat.version.name == "§4● Offline":
            embed.description = "We are not able to gather info from offline servers, sorry!\nProtocol Latency: " + str(
                round(
                    stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        elif stat.version.name == "⚠ Error":
            embed.description = "Server does not exist\nProtocol Latency: " + str(round(
                stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        elif stat.version.name == "§4● Starting":
            embed.description = "We are not able to gather info from starting servers, sorry!\nProtocol Latency: " + str(
                round(
                    stat.latency)) + "ms\n\nIf you believe this is wrong, please [join our discord server](https://discord.gg/G2AaJbvdHT)."
            embed.colour = Colors.red
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        else:
            embed.add_field(name="**__Status__**", value="Online", inline=True)
            embed.add_field(name="**__Players__**", value=str(stat.players.online) + "/" + str(stat.players.max),
                            inline=True)
            embed.add_field(name="**__Software__**", value=stat.version.name, inline=True)
            embed.add_field(name="**__MOTD__**", value=remove_colors_from_string(stat.description), inline=False)
            embed.colour = Colors.green
            embed.timestamp = dutils.utcnow()
            embed.set_footer(text="Command executed by " + ctx.author.name + "#" + ctx.author.discriminator)
        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Status(bot))
