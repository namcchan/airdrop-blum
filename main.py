import asyncio
from bot.coinsweeper import Coinsweeper
from bot.core import create_sessions
from bot.telegram import Accounts
from bot.blum import Blum
from bot.settings import settings
import os

hello = """

 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗     ██████╗  ██████╗ ████████╗███████╗
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝    ██████╔╝██║   ██║   ██║   ███████╗
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝     ██╔══██╗██║   ██║   ██║   ╚════██║
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║         ██████╔╝╚██████╔╝   ██║   ███████║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝

"""

async def main():
    print(hello)
    action = int(input('Select an action:\n1. Start collecting coins\n2. Create a session\n>'))

    if not os.path.exists('sessions'):
        os.mkdir('sessions')

    if action == 2:
        await create_sessions()

    if action == 1:

        bot = int(input("Select bot:\n1. Blum\n2. CoinSweeper\n>"))
        accounts = await Accounts().get_accounts()
        tasks = []
        if settings.USE_PROXY:
            proxies = []
            if not os.path.exists('proxy.txt'):
                with open('proxy.txt', 'w', encoding='utf-8') as file:
                    file.write('')
                proxies = []
            else:
                with open('proxy.txt','r',encoding='utf-8') as file:
                    proxies = [i.strip() for i in file.readlines()]

            for thread, account in enumerate(accounts):
                if bot == 1:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxies[thread % len(proxies)]).run()))
                elif bot == 2:
                    tasks.append(asyncio.create_task(Coinsweeper(account=account, thread=thread, proxy=proxies[thread % len(proxies)]).run()))
        else:
            for thread, account in enumerate(accounts):
                if bot == 1:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).run()))
                elif bot == 2:
                    tasks.append(asyncio.create_task(Coinsweeper(account=account, thread=thread,proxy = None).run()))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
