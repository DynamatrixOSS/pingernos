from re import sub
from json import load, decoder
from os import getenv
from sys import exit as sysexit
import mysql.connector as mysql

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print('You did not install the dotenv module! You will not be able to use a .env file.')
try:
    from mcstatus import JavaServer
    from mcstatus.pinger import PingResponse
except ModuleNotFoundError:
    print('You did not install the mcstatus module! Exiting now...')
    sysexit()


class Utils:
    @staticmethod  # This is a static method, you can call it without creating an instance of the class, but does not have access to the class or its attributes (self)
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
        usejson = True  # Set to True to a config.json
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
        if not usejson:
            try:
                data = {
                    "Token": getenv('TOKEN'),
                    "Prefix": getenv('PREFIX'),
                    "Owners": getenv('OWNERS').split(','),
                    "FeatureGuilds": getenv('FEATURE_GUILDS').split(','),
                    "Database": {
                        "Host": getenv('DB_HOST'),
                        "User": getenv('DB_USER'),
                        "Password": getenv('DB_PASSWORD'),
                        "Database": getenv('DB_DATABASE'),
                        "Port": getenv('DB_PORT')
                    },
                    "Logs": {
                        "JoinWebhook": getenv('LOGS_JOINWEBHOOK'),
                        "LeaveWebhook": getenv('LOGS_LEAVEWEBHOOK')
                    }
                }
            except AttributeError:
                print('You did not fill out the environment variables! Exiting now...')
                sysexit()
        return data

    @staticmethod
    async def get_server_status(serverip: str) -> PingResponse:
        server = await JavaServer.async_lookup(serverip)
        stat = await server.async_status()
        return stat

    @staticmethod
    async def mysql_login():
        data = Utils.get_data()

        return mysql.connect(
            host=data['Database']['Host'],
            user=data['Database']['User'],
            password=data['Database']['Password'],
            database=data['Database']['Database'])
