from loguru import logger
from bot.settings import settings
import pyrogram
import random

async def create_sessions():
    while True:
        session_name = input('Enter the session name (press Enter to exit)\n')
        if not session_name:
            return

        if settings.USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r') as file:
                proxy_list = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox,name in proxy_list:
                    proxy_dict[name] = prox

            if session_name in proxy_dict:
                proxy = proxy_dict[session_name]
                proxy_client = {
                    "scheme": settings.PROXY_TYPE,
                    "hostname": proxy.split(':')[0],
                    "port": int(proxy.split(':')[1]),
                    "username": proxy.split(':')[2],
                    "password": proxy.split(':')[3],
                }

                session = pyrogram.Client(
                    api_id=settings.API_ID,
                    api_hash=settings.API_HASH,
                    name=session_name,
                    workdir=settings.WORKDIR,
                    proxy=proxy_client
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Session added +{user_data.phone_number} @{user_data.username} PROXY {proxy.split(":")[0]}')
            else:

                session = pyrogram.Client(
                    api_id=settings.API_ID,
                    api_hash=settings.API_HASH,
                    name=session_name,
                    workdir=settings.WORKDIR
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Session added +{user_data.phone_number} @{user_data.username} PROXY : NONE')
        else:

            session = pyrogram.Client(
                api_id=settings.API_ID,
                api_hash=settings.API_HASH,
                name=session_name,
                workdir=settings.WORKDIR
            )

            async with session:
                user_data = await session.get_me()

            logger.success(f'Session added +{user_data.phone_number} @{user_data.username} PROXY : NONE')
