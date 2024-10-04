from loguru import logger
from bot.settings import settings
import pyrogram

async def create_sessions():
    while True:
        session_name = input('Enter the session name (press Enter to exit)\n')
        if not session_name:
            return

        session = pyrogram.Client(
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            name=session_name,
            workdir=settings.WORKDIR
        )
        async with session:
            user_data = await session.get_me()

        logger.success(f'Session added +{user_data.phone_number} @{user_data.username}')
