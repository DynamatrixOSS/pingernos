class Directories:
    migrations = "database/migrations"
    seeders = "database/seeders"
    modules = "app.commands"  # always use periods instead of slashes as this is how py-cord interprets the file paths for extensions.

    def get_directory(self, directory):
        return getattr(self, directory)

    def get_directories(self):
        return self
