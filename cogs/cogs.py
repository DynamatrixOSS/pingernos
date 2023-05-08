from os import listdir
from discord.ext.commands import slash_command
from discord.ext import commands
from discord import Option
from utils import Utils
from discord.ext.bridge import Bot
from discord.ext.bridge.context import BridgeContext

class Cogs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.info = Utils.get_data()

    def getcogs(self, ctx: BridgeContext) -> list | str:
        if ctx.interaction.user.id not in self.info['Owners']:
            return ["You are not an owner of the bot!"]
        cogs = []
        for file in listdir("./cogs"):
            if file.endswith(".py"):
                cogs.append(file[:-3])
        return cogs

    @slash_command(description='Only the owners of the bot can run this command',
                   guild_ids=Utils.get_data()['FeatureGuilds'])
    async def cogs(self, ctx: BridgeContext, action: Option(choices=["Load", "Unload", "Reload"]), cog: Option(autocomplete=getcogs)):
        if ctx.author.id not in self.info['Owners']:
            return
        if cog.lower() not in [f"{fn[:-3]}" for fn in listdir("./cogs")]:
            await Utils.respond(ctx, "That cog doesn't exist!", ephemeral=True)
            return
        if action.lower() not in ["load", "unload", "reload"]:
            await Utils.respond(ctx, "That action doesn't exist!", ephemeral=True)
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
            await Utils.respond(ctx, f"An error has occured!\n{error}")
            raise error
        try:
            await self.bot.sync_commands()
        except Exception as error:
            await Utils.respond(ctx, f"An error has occured!\n{error}")
            raise error
        await Utils.respond(ctx, f"{action}ed {cog} and reloaded all commands!")

def setup(bot: Bot):
    bot.add_cog(Cogs(bot))
