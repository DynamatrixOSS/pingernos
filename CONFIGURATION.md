# Configuration
Pingernos py offers three different ways to configure it, a config file, environment variables and a .env
If you wish to use the config file, you must set the `use_json` variable in [getdata](./utilities/data.py) to `True` and copy the [example.config.json](./example.config.json) to a new file called config.json in the root folder and modify the options in it.
If you wish to use a .env file, just copy the [example.env](./example.env) to a new file called .env in the root folder and modify the options in it, you can use environment variables and a .env file at the same time if you so desire.
Environment variables use `SCREAMING_SNAKE_CASE` while the configuration file uses `PascalCase`.

If a config file is missing, pingernos will try to load the environment variables. If both are missing, pingernos will exit.

## Auth Token (required)
Discord bot authentication token, can be generated in the [Developer Portal](https://discord.com/developers/applications/)

| type   | config file | environment |
|--------|-------------|-------------|
| string | `Token`     |  `TOKEN`    |

## Prefix (required)
Prefix to use for commands, can be a mention or a string

| type   | config file | environment |
|--------|-------------|-------------|
| string |  `Prefix`   | `PREFIX`    |

## Owners (required)
Array of user ids that are allowed to use owner only features

| type     | config file | environment |
|----------|-------------|-------------|
| string[] | `Owners`    | `OWNERS`    |

## FeatureGuilds (required)
Array of guild ids that are allowed to use owner only features

| type     | config file      | environment      |
|----------|------------------|------------------|
| string[] |  `FeatureGuilds` | `FEATURE_GUILDS` |

## Logs (required)

### JoinWebhook (required)
Webhook to send join logs to

| type   | config file        | environment        |
|--------|--------------------|--------------------|
| string | `Logs.JoinWebhook` | `LOGS_JOINWEBHOOK` |

### LeaveWebhook (required)
Webhook to send leave logs to

| type   | config file         | environment         |
|--------|---------------------|---------------------|
| string | `Logs.LeaveWebhook` | `LOGS_LEAVEWEBHOOK` |

## Database (required)
MySQL/MariaDB access credentials. Other SQL dialects or Databases are not supported.

### Host
Database hostname or IP

| type   | config file     | environment |
|--------|-----------------|-------------|
| string | `Database.Host` | `DB_HOST`   |

### User
Database username

| type   | config file     | environment |
|--------|-----------------|-------------|
| string | `Database.User` | `DB_USER`   |

### Password
Database password

| type   | config file         | environment   |
|--------|---------------------|---------------|
| string | `Database.Password` | `DB_PASSWORD` |

### Database
Database name

| type   | config file         | environment   |
|--------|---------------------|---------------|
| string | `Database.Database` | `DB_DATABASE` |

### Port
Database port

| type   | config file     | environment |
|--------|-----------------|-------------|
| int    | `Database.Port` | `DB_PORT`   |