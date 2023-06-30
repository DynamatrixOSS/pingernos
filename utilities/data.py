from re import sub
from json import load, decoder
from os import getenv
from sys import exit as sysexit

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


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a


def remove_colors_from_string(text) -> str:
    text = sub(r"§[0-9a-r]", "", text)
    return text


def get_data() -> dict:
    """
    This function is used to get the data from the config.json file.
    If you do not have a config.json file, you can use environment variables.
    :return: The data from the config.json file.
    """
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


async def get_server_status(serverip: str) -> PingResponse:
    """
    This function is used to get the status of a server.
    :param serverip: The ip of the server.
    :return: The status of the server.
    """
    server = await JavaServer.async_lookup(serverip)
    stat = await server.async_status()
    return stat
