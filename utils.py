from re import sub
from json import load, decoder
from os import getenv
from sys import exit as sysexit
from discord.ext.commands import HelpCommand
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print('You did not install the dotenv module! You will not be able to use a .env file.')
try:
    from mcstatus import JavaServer
except ModuleNotFoundError:
    print('You did not install the mcstatus module! Exiting now...')
    sysexit()
class Utils:
    @staticmethod #This is a static method, you can call it without creating an instance of the class, but does not have access to the class or its attributes (self)
    def remove_colors_from_string(text) -> str:
        text = sub(r"§[0-9a-r]", "", text)
        return text
    class Colors:
        blue = 0xadd8e6
        red = 0xf04747
        green = 0x90ee90
        orange = 0xfaa61a
    @staticmethod
    def get_data() -> dict:
        usejson = False #Set to True to a config.json
        if usejson:
            try:
                with open('config.json', 'r', encoding="UTF-8") as file:
                    data = load(file)
            except FileNotFoundError:
                print('config.json not found! Exiting now...')
                sysexit()
            except decoder.JSONDecodeError:
                print('config.json is not valid! Exiting now...')
                sysexit()
            except EncodingWarning:
                print('config.json is not encoded in UTF-8! Exiting now...')
                sysexit()
        if not usejson:
            #If you don't fill out the environment variables, it will return empty and probably crash, so make sure you fill them out!
            data = {
                "Token": getenv('TOKEN'),
                "Prefix": getenv('PREFIX'),
                "Owners": getenv('OWNERS').split(','),
                "Database": {
                    "Host": getenv('DB_HOST'),
                    "User": getenv('DB_USER'),
                    "Password": getenv('DB_PASSWORD'),
                    "Database": getenv('DB_DATABASE'),
                    "Port": getenv('DB_PORT')
                }
            }
        return data
    @staticmethod
    async def get_server_status(serverip: str) -> dict:
        server = await JavaServer.async_lookup(serverip)
        stat = await server.async_status()
        return stat

    class Help_Cmd(HelpCommand):
        async def send_bot_help(self, mapping):
            channel = self.get_destination()
            await channel.send("Type in **/** to see the commands!")
