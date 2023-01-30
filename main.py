from discord import Intents, Status, Activity, ActivityType
from discord.ext.bridge import Bot
from utils import Utils
data = Utils.get_data()
intents = Intents(guilds=True, guild_messages=True)
#intents.message_content = True #Uncomment this if you use prefixed command that are not mentions
bot = Bot(intents=intents, command_prefix=data['Prefix'], status=Status.dnd, activity=Activity(type=ActivityType.playing, name="Booting..."))
bot.load_extensions("cogs") #Loads all cogs in the cogs folder
@bot.event
async def on_connect():
    print('Connected to Discord!')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="you (prefix: @mention)"), status=Status.dnd)

bot.run(data['Token'])
