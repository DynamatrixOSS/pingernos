from config.app import Settings
import aiomysql
import asyncio


class DBPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure pool is initialized only once
            self.pool = None
            self.initialized = False

    async def init_pool(self):
        if not self.initialized:
            database_config = Settings.get_database()
            self.pool = await aiomysql.create_pool(
                host=database_config.get('host', 'localhost'),
                port=database_config.get('port', 3306),
                user=database_config.get('user', 'admin'),
                password=database_config.get('password', ''),
                db=database_config.get('database', 'test'),
                loop=asyncio.get_event_loop(),
                autocommit=True,
                maxsize=10,  # Adjust the pool size as needed
            )
            self.initialized = True

    async def close_pool(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
            self.initialized = False

    def get_pool(self):
        return self.pool


# Instantiate and export a single instance
db_pool = DBPool()
