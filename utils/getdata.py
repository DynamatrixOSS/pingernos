def getdata():
    usejson = True #Set to False to use enviorment variables instead of config.json
    if usejson:
        import json
        try:
            with open('utils/config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print('config.json not found! Exiting now...')
            exit()
        except json.decoder.JSONDecodeError:
            print('config.json is not valid! Exiting now...')
            exit()
    if not usejson:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ModuleNotFoundError:
            print('You did not install the dotenv module! You will not be able to use a .env file.')
        import os
        #If you don't fill out the environment variables, it will return empty and probably crash, so make sure you fill them out!
        return {
            "Token": os.getenv('TOKEN'),
            "Prefix": os.getenv('PREFIX'),
            "Owners": os.getenv('OWNERS').split(','),
            "Database": {
                "Host": os.getenv('DB_HOST'),
                "User": os.getenv('DB_USER'),
                "Password": os.getenv('DB_PASSWORD'),
                "Database": os.getenv('DB_DATABASE'),
                "Port": os.getenv('DB_PORT')
            }
        }