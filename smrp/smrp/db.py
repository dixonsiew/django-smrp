import asyncpg

pool: asyncpg.Pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost/smrpdb_uat")
    
async def close_db():
    global pool
    if pool:
        await pool.close()