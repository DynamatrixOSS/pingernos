from os import listdir
from discord.ext.commands import slash_command
from discord.ext import commands
from utils import Utils
class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info = Utils.get_data()

    @slash_command(description='Only the owners of the bot can run this command', guild_ids=[773950337303314518])
    async def cogs(self, ctx, action, cog):
        if ctx.author.id not in self.info['Owners']:
            return
        if cog.lower() not in [f"{fn[:-3]}" for fn in listdir("./cogs")]:
            await ctx.respond("That cog doesn't exist!", ephemeral=True)
            return
        if action.lower() not in ["load", "unload", "reload"]:
            await ctx.respond("That action doesn't exist!", ephemeral=True)
            return
        try:
            if action.lower() == "load":
                self.bot.load_extension(f"cogs.{cog}")
            if action.lower() == "unload":
                self.bot.unload_extension(f"cogs.{cog}")
            if action.lower() == "reload":
                self.bot.reload_extension(f"cogs.{cog}")
        except Exception as error:
            await ctx.respond(f"```py\n{error}\n```")
            return
        await ctx.respond(f"{action}ed {cog}")

def setup(bot):
    bot.add_cog(Cogs(bot))
