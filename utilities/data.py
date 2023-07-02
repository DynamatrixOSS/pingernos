from re import sub
from json import load, decoder
from os import getenv
from sys import exit as sysexit

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("You did not install the dotenv module! .env files can not be used.")
    dotenv_installed = False
try:
    from mcstatus import JavaServer
    from mcstatus.pinger import PingResponse
except ModuleNotFoundError:
    sysexit('You did not install the mcstatus module! Exiting now...')


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
    try:
        with open('config.json', 'r', encoding="UTF-8") as file:
            data = load(file)
    except FileNotFoundError:
        print("No config.json file found. Trying to use dotenv...")
        if not dotenv_installed:
            sysexit('You did not install the dotenv module and no config.json was provided! Exiting now...')
        else:
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
                sysexit('One or more environment variables could be found. Exiting now...')
    except decoder.JSONDecodeError:
        sysexit('config.json is not valid! Exiting now...')
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
