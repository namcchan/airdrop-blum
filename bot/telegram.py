from bot.core import logger
from pyrogram import Client
from bot.settings import settings as config
import os

class Accounts:
    def __init__(self):
        self.workdir = config.WORKDIR
        self.api_id = config.API_ID
        self.api_hash = config.API_HASH

    def pars_sessions(self):
        sessions = []
        for file in os.listdir(self.workdir):
            if file.endswith(".session"):
                sessions.append(file.replace(".session", ""))

        logger.info(f"Sessions found: {len(sessions)}!")
        return sessions

    async def check_valid_sessions(self, sessions: list):
        logger.info(f"Checking sessions for validity!")
        valid_sessions = []
        if config.USE_PROXY:
            proxies = []
            with open('proxy.txt','r') as file:
                proxies = [i.strip() for i in file.readlines()]
            for index in range(len(sessions)):
                try:
                    proxy = proxies[index % len(proxies)]
                    proxy_client = {
                        "scheme": config.PROXY_TYPE,
                            "hostname": proxy.split(':')[0],
                            "port": int(proxy.split(':')[1]),
                            "username": proxy.split(':')[2],
                            "password": proxy.split(':')[3],
                    }
                    client = Client(name=sessions[index], api_id=self.api_id, api_hash=self.api_hash, workdir=self.workdir,proxy=proxy_client)

                    if await client.connect():
                        valid_sessions.append(sessions[index])
                    else:
                        logger.error(f"{sessions[index]}.session is invalid")

                    await client.disconnect()
                except:
                    logger.error(f"{sessions[index]}.session is invalid")
            logger.success(f"Valid sessions: {len(valid_sessions)}; Invalid: {len(sessions)-len(valid_sessions)}")
        else:
            for index in sessions:
                try:
                    client = Client(name=index, api_id=self.api_id, api_hash=self.api_hash, workdir=self.workdir)

                    if await client.connect():
                        valid_sessions.append(index)
                    else:
                        logger.error(f"{index}.session is invalid")
                    await client.disconnect()
                except:
                    logger.error(f"{index}.session is invalid")
            logger.success(f"Valid sessions: {len(valid_sessions)}; Invalid: {len(sessions)-len(valid_sessions)}")
        return valid_sessions

    async def get_accounts(self):
        sessions = self.pars_sessions()
        accounts = await self.check_valid_sessions(sessions)

        if not accounts:
            raise ValueError("No valid sessions")
        else:
            return accounts
