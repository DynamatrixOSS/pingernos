class Directories:
    migrations = f"database/migrations"
    seeders = f"database/seeders"

    def get_directory(self, directory):
        return self.__getattribute__(directory)

    def get_directories(self):
        return self
