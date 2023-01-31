from discord.ext import commands#, bridge
class SetServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@bridge.bridge_command(aliases=["set"], description="Set the default server to use if no argument is provided in the status command.")
    #async def setserver(self, ctx, server = None):
    #    if server is None:
    #        return await ctx.respond("Please provide a server IP.")
    #    await ctx.defer()
        #This is up to Miataboy to implement

def setup(bot):
    bot.add_cog(SetServer(bot))
