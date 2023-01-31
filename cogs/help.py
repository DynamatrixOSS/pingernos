from discord.ext import commands
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        return await ctx.reply("Type in **/** to see the commands!")

def setup(bot):
    bot.add_cog(Help(bot))
