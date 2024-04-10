import discord
from discord.ext import commands


class Error(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.respond("That command doesn't exist!")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.respond("You need the `Manage Server` permission to use this command.")
        await ctx.respond("An unknown error has occurred!\nThis has been logged")
        raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, discord.CheckFailure):
            if not ctx.guild:
                return await ctx.respond("This command can only be used in a server.", ephemeral=True)
        if isinstance(error, commands.NotOwner):
            return await ctx.respond("This command is for owners only.")
        if isinstance(error, commands.GuildNotFound):
            return await ctx.respond("Could not find this guild.")
        await ctx.respond("An unknown error has occurred!\nThis has been logged")
        raise error


def setup(bot: discord.Bot):
    bot.add_cog(Error(bot))
