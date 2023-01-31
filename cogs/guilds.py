from discord.ext import commands, bridge
from discord import Embed
from utils import Utils
class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["servers"], description = "Shows how many guilds the bot is in.")
    async def guilds(self, ctx):
        embed = Embed()
        embed.description = f"{self.bot.user.name} is currently in {len(self.bot.guilds)} servers with a total of {sum(x.member_count for x in self.bot.guilds)} users."
        embed.color = Utils.Colors.blue
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Guilds(bot))
