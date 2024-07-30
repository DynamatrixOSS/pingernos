from config.vault import get_vault


class Settings:
    def __init__(self):
        self.environment = "development"
        self.debug = False
        self.seeding = False
        self.migrations = True

    def get_setting(self, setting):
        return self.__getattribute__(setting)

    def get_settings(self):
        return self

    def get_environment(self):
        return self.environment

    def set_environment(self, environment: str):
        allowed_environments = ["prod", "production", "development", "dev", "testing"]
        environment = environment.lower()
        if any(allowed_environment in environment for allowed_environment in allowed_environments):
            self.environment = environment
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
