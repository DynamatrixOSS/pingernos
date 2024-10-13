import warnings

import aiomysql
import pymysql

from database.executioners.initiator import db_pool
from providers.modifiers import logger


logger = logger.setup_logger()


async def execute(statement: str, args: [] = None):
    pool = db_pool.get_pool()

    if pool is None:
        raise ConnectionAbortedError('A connection with the pool could not be established as the pool could not be found')

    try:
        logger.debug(f'Executing statement: {statement} with args {args}')
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                with warnings.catch_warnings():
                    warnings.simplefilter('error')
                    await cursor.execute(statement, args)
                    await conn.commit()

                    if cursor.description:
                        column_names = [desc[0] for desc in cursor.description]
                        rows = await cursor.fetchall()
                        result = [dict(zip(column_names, row)) for row in rows]

                        return result

                    return []
    except pymysql.err.Warning:
        pass
    except aiomysql.Error as err:
        if conn.in_transaction:
            await pool.rollback()
        logger.error('An aiomysql error occurred while executing statement {} with args {} and was forcibly rolled back.\n{}'.format(statement, args, err))
    except Exception as err:
        if conn.in_transaction:
            await pool.rollback()
        logger.error('An unknown error occurred while executing statement {} with args {} and was forcibly rolled back.\n{}'.format(statement, args, err))
