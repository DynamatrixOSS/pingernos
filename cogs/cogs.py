from os import listdir

import discord
from discord import option
from discord.ext.commands import slash_command

from utilities.data import get_data


class Cogs(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.info = get_data()

    def get_cogs(self, ctx) -> list:
        if ctx.interaction.user.id not in self.info['Owners']:
            return ["You are not an owner of the bot!"]
        cogs = []
        for file in listdir("./cogs"):
            if file.endswith(".py"):
                cogs.append(file[:-3])
        return cogs

    @slash_command(guild_ids=get_data()['FeatureGuilds'])
    @option("action", choices=["Load", "Unload", "Reload"])
    @option("cog", autocomplete=get_cogs)
    async def cogs(self, ctx, action, cog):
        """ Only the owners of the bot can run this command """
        if ctx.author.id not in self.info['Owners']:
            return await ctx.respond("This command is for owners only.", ephemeral=True)
        if cog.lower() not in [f"{fn[:-3]}" for fn in listdir("./cogs")]:
            return await ctx.respond("That cog doesn't exist!")
        if action not in ["Load", "Unload", "Reload"]:
            return await ctx.respond("That action doesn't exist!")
        await ctx.defer()
        try:
            if action == "Load":
                self.bot.load_extension(f"cogs.{cog}")
            elif action == "Unload":
                self.bot.unload_extension(f"cogs.{cog}")
            elif action == "Reload":
                self.bot.reload_extension(f"cogs.{cog}")
        except Exception as error:
            await ctx.respond(f"An error has occurred!\n{error}")
            raise error
        try:
            await self.bot.sync_commands()
        except Exception as error:
            await ctx.respond(f"An error has occurred!\n{error}")
            raise error
        await ctx.respond(f"{action}ed {cog} and reloaded all commands!")


def setup(bot: discord.Bot):
    bot.add_cog(Cogs(bot))
