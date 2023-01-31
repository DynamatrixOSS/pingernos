from discord import Intents, Status, Activity, ActivityType
from discord.ext.bridge import Bot
from utils import Utils
data = Utils.get_data()
intents = Intents(guilds=True, guild_messages=True)
#intents.message_content = True #Uncomment this if you use prefixed command that are not mentions
bot = Bot(intents=intents, command_prefix=data['Prefix'], status=Status.dnd, activity=Activity(type=ActivityType.playing, name="you (prefix: @mention)"))
bot.load_extensions("cogs") #Loads all cogs in the cogs folder
bot.help_command = Utils.help_cmd #Disables the default help command
BOOTED = False
@bot.listen()
async def on_connect():
    print('Connected to Discord!')

@bot.listen()
async def on_ready():
    global BOOTED
    if not BOOTED:
        await bot.sync_commands()
        print(f'Logged in as {bot.user}')
        print('------')
        BOOTED = True
    if BOOTED:
        print ("Reconnect(?)")

bot.run(data['Token'])
