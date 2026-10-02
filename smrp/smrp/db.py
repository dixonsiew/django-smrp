import asyncpg
from pymongo import MongoClient
from django.conf import settings

pool: asyncpg.Pool = None
client: MongoClient = None

async def init_db():
    global pool, client
    pool = await asyncpg.create_pool(f"postgresql://postgres:postgres@localhost/{settings.POSTGRES_DB}")
    client = MongoClient("mongodb://localhost:27017/")

async def close_db():
    global pool
    if pool:
        await pool.close()
        
    global client
    if client:
        client.close()