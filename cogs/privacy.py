from discord.ext import commands, bridge
from discord import Embed
from utils import Utils
class Privacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description = "Shows the privacy policy of the bot.")
    async def privacy(self, ctx):
        embed = Embed()
        embed.description = f"{self.bot.user.name} saves a minimal amount of data to allow for its functionality. Full information about what is collected can be found on [W.I.P. bear with us]. For any concerns, Mail to soapy@cloudykingdom.com"
        embed.color = Utils.Colors.blue
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Privacy(bot))
