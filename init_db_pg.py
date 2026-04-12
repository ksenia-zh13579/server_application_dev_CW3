import asyncpg
import asyncio

import config

async def create_table():
    conn = await asyncpg.connect(config.database_url)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    await conn.close()

asyncio.run(create_table())