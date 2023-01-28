from discord import Intents, Status, Activity, ActivityType
from discord.ext import commands
from utils.getdata import getdata
data = getdata()
intents = Intents(guilds=True, guild_messages=True)
#intents.message_content = True #Uncomment this if you use prefixed command that are not mentions (e.g. !help)
bot = commands.Bot(intents=intents, command_prefix=data['Prefix'], status=Status.dnd, activity=Activity(type=ActivityType.playing, name="Booting..."))
bot.remove_command('help') #Removes the default help command
bot.load_extensions("cogs") #Loads all cogs in the cogs folder
booted = False
@bot.event
async def on_connect():
    print('Connected to Discord!')

@bot.event
async def on_ready():
    global booted
    if booted is False:
        await bot.change_presence(activity=Activity(type=ActivityType.watching, name=f"you (prefix: @mention)"), status=Status.dnd)
        booted = True #This is to prevent the bot from changing its presence every time it reconnects, even though this is in general a bad coding practice to redefine an outside variable in a function.
    print(f'Logged in as {bot.user}')
    print('------')

bot.run(data['Token'])