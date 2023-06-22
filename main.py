from discord import Intents, Status, Activity, ActivityType
from discord.ext.bridge import AutoShardedBot
from utils import Utils

data = Utils.get_data()
intents = Intents(guilds=True, guild_messages=True)
# intents.message_content = True #Uncomment this if you use prefixed command that are not mentions
bot = AutoShardedBot(intents=intents, command_prefix=data['Prefix'], status=Status.dnd,
          activity=Activity(type=ActivityType.watching, name="Starting..."))
bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
bot.help_command = Utils.HelpCmd()  # Disables the default help command
BOOTED = False

@bot.listen()
async def on_connect():
    print('Connected to Discord!')
    cursor = await Utils.mysql_login()
    database = cursor.cursor()
    database.execute("CREATE TABLE IF NOT EXISTS server (guild_id VARCHAR(255) PRIMARY KEY, server_ip TEXT NOT NULL)")
    database.execute("CREATE TABLE IF NOT EXISTS blacklist (guild_id VARCHAR(21) PRIMARY KEY, reason TEXT NOT NULL)")
    database.close()

@bot.listen()
async def on_reconnect():
    print('Reconnected to Discord!')

@bot.listen()
async def on_ready():
    global BOOTED #I'm sorry, but there's no other way to do this without classes which I want only in the cogs
    if BOOTED:
        print("Reconnect(?)")
    if not BOOTED:
        # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user} with {bot.shard_count+1} shards!')
        print('------')
        for shard in bot.shards:
            await bot.change_presence(status=Status.dnd, activity=Activity(type=ActivityType.watching, name=f"you (prefix: @mention) | Shard: {shard+1}"), shard_id=shard)
        BOOTED = True

bot.run(data['Token'])
