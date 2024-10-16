from asyncio import wait_for

import discord
from discord import slash_command, Embed

from utilities.data import Colors, get_server_status


class Info(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    async def info(self, ctx):
        """ Displays information about Pingernos """
        embed = Embed()
        try:
            stat = await wait_for(get_server_status("example.aternos.me"), timeout=2)
        except TimeoutError:
            latency = "N/A"
        else:
            latency = round(stat.latency)
        embed.description = f"""
{self.bot.user.name} is a bot developed by Blue Atomic to service Aternos users by displaying server statuses. We are not affiliated with Aternos and are an independent FOSSDEV organization.

**Guilds:** {len(self.bot.guilds)}
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**Protocol Latency:** {latency}ms
**Shard count:** {self.bot.shard_count}
**Shard:** {ctx.guild.shard_id + 1}

[[Invite]](https://discord.com/api/oauth2/authorize?client_id=889197952994791434&permissions=274878286912&scope=bot%20applications.commands) [[Support]](https://discord.gg/Ukr89GrMBk) [[Github]](https://github.com/BlackFurORG/pingernos) [[Privacy Policy]](https://gist.github.com/MiataBoy/20fda9024f277ea5eb2421adbebc2f23) [[Terms of Service]](https://gist.github.com/MiataBoy/81e96023a2aa055a038edab02e7e7792)
        """
        embed.colour = Colors.blue
        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Info(bot))
