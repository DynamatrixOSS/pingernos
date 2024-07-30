class Directories:
    migrations = "database/migrations"
    seeders = "database/seeders"

    def get_directory(self, directory):
        return getattr(self, directory)

    def get_directories(self):
        return self
