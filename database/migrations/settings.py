class Schema:
    name = "guild_settings"
    columns = [
        "guild_id VARCHAR(26) PRIMARY KEY",
        "name VARCHAR(255)",
        "language VARCHAR(4) DEFAULT 'en'",
    ]

    def get_name(self):
        return self.name

    def get_columns(self):
        return self.columns
