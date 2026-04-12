'''
import asyncpg

import config

async def get_db_connection_postgres():
    conn = await asyncpg.connect(config.database_url)
    try:
        yield conn
    finally:
        await conn.close()
'''
from databases import Database

import config

database = Database(config.database_url)