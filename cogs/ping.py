from discord.ext import commands, bridge
from asyncio import wait_for
from utils import Utils
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["latency", "pong"], description="Get the bot and websocket latency")
    async def ping(self, ctx):
        await ctx.defer()
        try:
            stat = await wait_for(Utils.get_server_status("example.aternos.me"), timeout=3)
        except TimeoutError:
            return await ctx.respond(f"Uh oh! The protocol took too long to respond! This will likely fix itself.\nAPI Latency is {round(self.bot.latency*1000, 2)}ms")
        await ctx.respond(content=f"API Latency is {round(self.bot.latency*1000, 2)}ms\nProtocol: {round(stat.latency)}ms")

def setup(bot):
    bot.add_cog(Ping(bot))
