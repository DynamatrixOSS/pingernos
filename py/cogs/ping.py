from discord.ext import commands
from mcstatus import JavaServer
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.reply('Calculating ping...')
        server = await JavaServer.async_lookup("example.aternos.me")
        #Wait for it to finish
        stat = await server.async_status()
        #async with aiohttp.ClientSession() as session:
        #    async with session.get("example.aternos.me") as response:
        #        await response.json()
        #print (msg.created_at.timestamp(), ctx.message.created_at.timestamp())
        await msg.edit(content=f"""🏓 Latency is {round(msg.created_at.timestamp()-ctx.message.created_at.timestamp(), 2)}ms
API Latency is {round(self.bot.latency*1000, 2)}ms
Protocol: {round(stat.latency)}ms""")
        
def setup(bot):
    bot.add_cog(Ping(bot))