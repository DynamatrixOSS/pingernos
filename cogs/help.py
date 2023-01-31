from discord.ext import commands
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        return

def setup(bot):
    bot.add_cog(Ping(bot))
