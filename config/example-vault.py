class Vault:
    def __init__(self):
        self.token = "token"
        self.hostname = "hostname"
        self.database = {
            "host": "localhost",
            "user": "user",
            "password": "password",
            "database": "database",
        }


vault_instance = Vault()


def get_vault():
    return vault_instance
