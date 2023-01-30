from discord.ext import commands, bridge
from mcstatus import JavaServer
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Get the bot ping")
    async def ping(self, ctx):
        await ctx.defer()
        server = await JavaServer.async_lookup("example.aternos.me")
        stat = await server.async_status()
        await ctx.respond(content=f"API Latency is {round(self.bot.latency*1000, 2)}ms\nProtocol: {round(stat.latency)}ms")

def setup(bot):
    bot.add_cog(Ping(bot))
