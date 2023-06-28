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
        """
        This function is used to get the data from the config.json file.
        If you do not have a config.json file, you can use environment variables.
        :return: The data from the config.json file.
        """
        usejson = False  # Set to True to a config.json
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
        """
        This function is used to get the status of a server.
        :param serverip: The ip of the server.
        :return: The status of the server.
        """
        server = await JavaServer.async_lookup(serverip)
        stat = await server.async_status()
        return stat

    @staticmethod
    async def mysql_login():
        """
        This function is used to login to the database.
        :return: The cursor to use for queries.
        """
        database = Utils.get_data()['Database']

        return mysql.connect(
            host=database['host'],
            user=database['user'],
            password=database['password'],
            database=database['database'])

    @staticmethod
    async def selector(query: str, variables: list):
        """
        This function is used to select data from the database. It is used for SELECT queries.
        :param query: The query to execute. Use %s for variables. Example: "SELECT * FROM table WHERE column = %s"
        :param variables: The variables to use in the query. If there are no variables, use an empty list.
        :return: The result of the query. If there is no result, it will return False.
        """
        cursor = await Utils.mysql_login()
        db = cursor.cursor()
        db.execute(query, variables)
        try:
            result = db.fetchall()[0]
        except IndexError:
            return False
        db.close()
        cursor.close()
        return result

    @staticmethod
    async def modifyData(query: str, variables: list) -> None:
        """
        This function is used to modify data in the database. It is used for INSERT, UPDATE, and DELETE queries.
        :param query: The query to execute. Use %s for variables. Example: "INSERT INTO table (column) VALUES (%s)"
        :param variables: The variables to use in the query. If there are no variables, use an empty list.
        :return: None
         """
        cursor = await Utils.mysql_login()
        db = cursor.cursor()
        db.execute(query, variables)
        cursor.commit()
        db.close()
        cursor.close()
