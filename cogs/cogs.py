from os import listdir
import discord
from discord.ext.commands import slash_command
from discord import Option
from discord.ext.bridge import Bot
from utilities.data import get_data


class Cogs(discord.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.info = get_data()

    def getcogs(self, ctx) -> list:
        if ctx.interaction.user.id not in self.info['Owners']:
            return ["You are not an owner of the bot!"]
        cogs = []
        for file in listdir("./cogs"):
            if file.endswith(".py"):
                cogs.append(file[:-3])
        return cogs

    @slash_command(description='Only the owners of the bot can run this command', guild_ids=get_data()['FeatureGuilds'])
    async def cogs(self, ctx, action: Option(choices=["Load", "Unload", "Reload"]), cog: Option(autocomplete=getcogs)):
        if ctx.author.id not in self.info['Owners']:
            return
        if cog.lower() not in [f"{fn[:-3]}" for fn in listdir("./cogs")]:
            await ctx.respond("That cog doesn't exist!")
            return
        if action.lower() not in ["load", "unload", "reload"]:
            await ctx.respond("That action doesn't exist!")
            return
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


def setup(bot: Bot):
    bot.add_cog(Cogs(bot))
