from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

client = None
database = None
async def connect_db():
    global client, database
    cfg = get_settings(); client = AsyncIOMotorClient(cfg.mongodb_uri, serverSelectionTimeoutMS=10000)
    await client.admin.command("ping"); database = client[cfg.mongodb_database]
    await database.users.create_index("email", unique=True)
    await database.scans.create_index([("user_id", 1), ("created_at", -1)])
async def close_db():
    if client: client.close()
