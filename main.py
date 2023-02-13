from discord import Intents, Status, Activity, ActivityType
from discord.ext.bridge import Bot
from utils import Utils
import mysql.connector as mysql

data = Utils.get_data()
intents = Intents(guilds=True, guild_messages=True)
#intents.message_content = True #Uncomment this if you use prefixed command that are not mentions
bot = Bot(intents=intents, command_prefix=data['Prefix'], status=Status.dnd, activity=Activity(type=ActivityType.watching, name="you (prefix: @mention)"))
bot.load_extensions("cogs") #Loads all cogs in the cogs folder
bot.help_command = Utils.HelpCmd() #Disables the default help command
BOOTED = False
@bot.listen()
async def on_connect():
    print('Connected to Discord!')
    await Utils.mysql_connection("CREATE TABLE IF NOT EXISTS servers (guild_id VARCHAR(255) PRIMARY KEY, server_ip TEXT NOT NULL)")

@bot.listen()
async def on_ready():
    global BOOTED
    if BOOTED:
        print ("Reconnect(?)")
    if not BOOTED:
        #await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user}')
        print('------')
        BOOTED = True

bot.run(data['Token'])
