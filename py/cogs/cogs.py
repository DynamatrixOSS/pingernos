from discord.ext import commands
from utils.getdata import getdata
import os

class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info = getdata()

    @commands.command(description='Only the owner of the bot can run this command')
    async def cogs(self, ctx, action, cog): #folder: discord.Option(autocomplete=getfolders)
        if ctx.guild.id != 955135608228024394:
            return
        if ctx.author.id not in self.info['Owners']:
            return
        if cog.lower() not in [f"{fn[:-3]}" for fn in os.listdir("./cogs")]:
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
        except Exception as e:
            await ctx.reply(f"```py\n{e}\n```", mention_author=False)
            return
        await ctx.reply(f"{action}ed {cog}", mention_author=False)
        
def setup(bot):
    bot.add_cog(Cogs(bot))
