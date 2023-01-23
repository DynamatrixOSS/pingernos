# Configuration
Pingernos py offers three different ways to configure it, a config file, environment variables and a .env
If you wish to use the config file, just copy the [example.config.json](./utils/data/example.config.json) to a new file called config.json in the utils/data folder and modify the options in it.
If you wish to use environment variables, you must set the `usejson` variable in [getdata](./utils/data/getdata.py) to `False`.
If you wish to use a .env file, just copy the [example.env](./utils/data/example.env) to a new file called .env in the utils/data folder and modify the options in it, you can use environment variables and a .env file at the same time if you so desire.
Environment variables use `SCREAMING_SNAKE_CASE`, the configuration file uses `PascalCase`.

If a config file is missing, pingernos will try to load the environment variables. If both are missing, pingernos will exit.

## Auth Token (required)
Discord bot authentication token, can be generated in the [Developer Portal](https://discord.com/developers/applications/)

| type   | config file | environment         |
|--------|-------------|---------------------|
| string | `Token` | `TOKEN` |

## Prefix (required)
Prefix to use for commands, can be a mention or a string

| type   | config file | environment         |
|--------|-------------|---------------------|
| string | `Prefix` | `PREFIX` |

## Owners (required)
Array of user ids that are allowed to use owner only features

| type     | config file        | environment                |
|----------|--------------------|----------------------------|
| string[] | `Owners` | `OWNERS` |

## Database (required)
MySQL/MariaDB access credentials. Other SQL dialects or Databases are not supported.

### Host
Database hostname or IP

| type   | config file     | environment            |
|--------|-----------------|------------------------|
| string | `Database.Host` | `DATABASE_HOST` |

### User
Database username

| type   | config file     | environment            |
|--------|-----------------|------------------------|
| string | `Database.User` | `DATABASE_USER` |

### Password
Database password

| type   | config file         | environment                |
|--------|---------------------|----------------------------|
| string | `Database.Password` | `DATABASE_PASSWORD` |

### Database
Database name

| type   | config file         | environment                |
|--------|---------------------|----------------------------|
| string | `Database.Database` | `DATABASE_DATABASE` |
