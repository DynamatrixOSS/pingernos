from asyncio import wait_for
from discord.ext import commands, bridge
from discord import Embed
from utils import Utils

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["information"], description = "Displays information about Pingernos")
    async def info(self, ctx):
        embed = Embed()
        try:
            stat = await wait_for(Utils.get_server_status("example.aternos.me"), timeout=2)
        except TimeoutError:
            latency = "N/A"
        else:
            latency = round(stat.latency)
        embed.description = f"""
{self.bot.user.name} is a bot developed by BlackFur Studios to service Aternos users by displaying server statuses. We are not affiliated with Aternos and are an independent FOSSDEV organization.

**Guilds:** {len(self.bot.guilds)}
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency*1000)}ms
**Protocol Latency:** {latency}ms

[[Support]](https://discord.gg/Ukr89GrMBk) [[Github]](https://github.com/BlackFurORG/pingernos)
        """
        embed.colour = Utils.Colors.blue
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
