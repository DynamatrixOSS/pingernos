from discord.ext import commands, bridge
from discord import Embed
from utils import Utils
class Privacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description = "Shows the privacy policy of the bot.")
    async def privacy(self, ctx):
        embed = Embed()
        embed.description = f"{self.bot.user.name} saves a minimal amount of data to allow for its functionality. As we work on regaining full functionality, we do not currently collect anything On our database storage, we currently only have server IPs and guild IDs stored. For any concerns, Mail to miataboymx@gmail.com or join https://discord.gg/Ukr89GrMBk"
        embed.colour = Utils.Colors.blue
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Privacy(bot))
