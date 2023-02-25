from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.respond("That command doesn't exist!")
        await ctx.respond("An unknown error has occured!\nThis has been logged")
        raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        await ctx.respond("An unknown error has occured!\nThis has been logged")
        raise error


def setup(bot):
    bot.add_cog(Error(bot))
