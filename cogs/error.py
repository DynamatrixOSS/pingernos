from discord.ext import commands
from discord.ext.bridge import Bot


class Error(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.respond("That command doesn't exist!")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.respond("You need the `Manage Server` permission to use this command.")
        await ctx.respond("An unknown error has occured!\nThis has been logged")
        raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            return await ctx.respond("This command is for owners only.")
        if isinstance(error, commands.GuildNotFound):
            return await ctx.respond("Could not find this guild.")
        await ctx.respond("An unknown error has occured!\nThis has been logged")
        raise error


def setup(bot: Bot):
    bot.add_cog(Error(bot))
