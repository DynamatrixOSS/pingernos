from config.vault import get_vault


class Settings:
    def __init__(self):
        self.settings = {
            "environment": "development",
            "debug": False,
            "seeding": False,
            "migrations": True,
            "manager_guilds": [1256003845188882562],
            "github": "https://github.com/DynamatrixOSS/pingernos",
            "discord": "https://discord.gg/Z8KGvGWZcY",
            "privacy": "https://rebel.dynamatrix.com/privacy",
            "invite": "https://rebel.dynamatrix.com/invite",
        }

    def get_setting(self, setting: str):
        return self.settings.get(setting, None)

    def set_setting(self, setting: str, value) -> None:
        self.settings[setting] = value

    def get_environment(self) -> str:
        return self.settings['environment']

    def set_environment(self, environment: str):
        allowed_environments = ["prod", "production", "development", "dev", "testing"]
        environment = environment.lower()
        if any(allowed_environment in environment for allowed_environment in allowed_environments):
            self.settings["environment"] = environment
            return {'message': 'Environment successfully set to {}'.format(environment), 'code': 200}

        raise ValueError('Environment {} is not valid. Must be one of following values: {}'.format(environment, allowed_environments))

    @staticmethod
    def get_token():
        vault = get_vault()
        return vault.token

    @staticmethod
    def get_hostname():
        vault = get_vault()
        return vault.hostname

    @staticmethod
    def get_database():
        vault = get_vault()
        return vault.database
