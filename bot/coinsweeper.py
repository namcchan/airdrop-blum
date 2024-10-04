

from datetime import datetime
import hashlib
import hmac
import math
from random import random
import sys
from time import time
import urllib.parse
import random
from bot import settings
from fake_useragent import UserAgent
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
import pytz
import aiohttp
from bot.core import logger
import time

def calc(i, s, a, o, d, g):
    st = (10 * i + max(0, 1200 - 10 * s) + 2000) * (1 + o / a) / 10
    return math.floor(st) + value(g)

def generate_hash(key, message):
    hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)

def value(input_str):
    return sum(ord(char) for char in input_str) / 1e5

class Coinsweeper:
    def __init__(self, thread: int, account: str, proxy : str):
        self.thread = thread
        self.name = account
        proxy_parts = proxy.split(':') if proxy else []
        proxy_client = {
            "scheme": settings.PROXY_TYPE,
            "hostname": proxy_parts[0],
            "port": int(proxy_parts[1]),
            "username": proxy_parts[2],
            "password": proxy_parts[3],
        } if len(proxy_parts) == 4 else None
        self.client = Client(name=account, api_id=settings.API_ID, api_hash=settings.API_HASH, workdir=settings.WORKDIR, proxy=proxy_client)

        if proxy:
            self.proxy = f"{settings.PROXY_TYPE}://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        else:
            self.proxy = None

        self.access_token = ""
        self.refresh_token = ""
        self.user_id = ""
        self.logged = False
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,vi-VN;q=0.6,vi;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bybitcoinsweeper.com",
            "Referer": "https://bybitcoinsweeper.com/",
            "tl-init-data": None,
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": UserAgent(os='android').random
        }
        self.session = aiohttp.ClientSession(headers=self.headers, trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False))

    def wait(self, seconds):
        for i in range(seconds, 0, -1):
            time.sleep(1)

    async def play_game(self, is_win=True):
        try:
            await self.get_me()
            min_game_time = settings.COINSWEEPER_TIME_PLAY_EACH_GAME[0]
            max_game_time = settings.COINSWEEPER_TIME_PLAY_EACH_GAME[1]
            game_time = random.randint(min_game_time, max_game_time)
            response = await self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers, proxy=self.proxy)
            playgame = await response.json()
            if "message" in playgame:
                if("expired" in playgame["message"]):
                    await self.do_refresh_token()
            gameid = playgame["id"]
            rewarddata = playgame["rewards"]
            started_at = playgame["createdAt"]
            unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
            starttime = int(unix_time_started.timestamp() * 1000)
            logger.info(f"Starting game {gameid}. Play time: {game_time} seconds")
            i = f"{self.user_id}v$2f1"
            first = f"{i}-{gameid}-{starttime}"
            last = f"{game_time}-{gameid}"
            score = calc(45, game_time, 54, 9, True, gameid)
            game_data = {
                "bagCoins": rewarddata["bagCoins"],
                "bits": rewarddata["bits"],
                "gifts": rewarddata["gifts"],
                "gameId": gameid,
                'gameTime': game_time,
                "h": generate_hash(first ,last),
                'score': float(score)
            }
            self.wait(game_time)
            if is_win:
                response = await self.session.post('https://api.bybitcoinsweeper.com/api/games/win', json=game_data, headers=self.headers, proxy=self.proxy)
                if response.status == 201:
                    logger.success(f"Game Status: WIN")
                elif response.status == 401:
                    logger.error(f"{self.name} | Token expired, need to refresh token")
                    await self.do_refresh_token()
                else:
                    logger.error(f"{self.name} | An Error Occurred With Code {response.status}")
            else:
                game_data = {
                    "bagCoins": rewarddata["bagCoins"],
                    "bits": rewarddata["bits"],
                    "gifts": rewarddata["gifts"],
                    "gameId": gameid
                }
                response = await self.session.post('https://api.bybitcoinsweeper.com/api/games/lose', json=game_data, headers=self.headers, proxy=self.proxy)
                if response.status == 201:
                    logger.error(f"Game Status: LOSEEEEEEEE")
                elif response.status == 401:
                    logger.error(f"{self.name} | Token expired, need to refresh token")
                    await self.do_refresh_token()
                else:
                    logger.error(f"{self.name} | An Error Occurred With Code {response.status}")
            self.wait(5)
        except Exception as e:
            logger.warning(f"{self.name} | {e}")
            self.wait(60)

    async def play(self):
        for i in range(3):
            try:
                is_win = random.random() < float(0.8)
                if(is_win):
                    await self.play_game(is_win=True)
                else:
                    await self.play_game(is_win=False)
            except Exception as e:
                logger.error(f"{self.name} | {e}")

    async def login(self):
        try:
            tg_web_data = await self.get_tg_web_data()
            if tg_web_data is None:
                sys.exit(0)
            response = await self.session.post(
                "https://api.bybitcoinsweeper.com/api/auth/login",
                json={"initData": tg_web_data},
                proxy=self.proxy
            )
            if response.status == 201:
                user_data = await response.json()
                self.access_token = user_data["accessToken"]
                self.refresh_token = user_data['refreshToken']
                self.session.headers['Authorization'] = f"Bearer {self.access_token}"
                self.logged = True
                logger.success(f"{self.name} | Logged in successfully")
            else:
                logger.error(f"{self.name} | {response.status}")
                await self.session.close()
        except Exception as err:
            logger.error(f"{self.name} | {err}")
            await self.session.close()
            if err == "Server disconnected":
                self.logged = False


    async def get_me(self):
        try:
            response = await self.session.get("https://api.bybitcoinsweeper.com/api/users/me", proxy=self.proxy)
            if response.status == 200:
                user = await response.json()
                self.user_id = user['id']
                logger.success(f"{self.name} | Balance: {user['score']}")
            else:
                logger.warning(f"{self.name} | Get user info failed: {response.status} | {response.json()}")
        except Exception as err:
            logger.error(f"{self.name} | {err}")

    async def do_refresh_token(self):
        payload = {
            "refreshToken": str(self.refresh_token)
        }
        response = await self.session.post("https://api.bybitcoinsweeper.com/api/auth/refresh-token", json=payload, proxy=self.proxy)
        if response.status == 201:
            token = await response.json()
            self.access_token = token['accessToken']
            self.refresh_token = token['refreshToken']
            self.session.headers['Authorization'] = f"Bearer {self.access_token}"
            logger.success(f"{self.name} | Refresh token successfully")
        else:
            logger.warning(f"{self.name} | Refresh token failed")

    async def get_tg_web_data(self):
        await self.client.connect()
        try:
            web_view = await self.client.invoke(RequestWebView(
                peer=await self.client.resolve_peer('BybitCoinsweeper_Bot'),
                bot=await self.client.resolve_peer('BybitCoinsweeper_Bot'),
                platform='android',
                from_bot_menu=False,
                url='https://bybitcoinsweeper.com'
            ))
            auth_url = web_view.url
            logger.success(f"{self.name} | Get tg web data successfully!")
        except Exception as err:
            logger.error(f"{self.name} | {err}")
            if 'USER_DEACTIVATED_BAN' in str(err):
                logger.error(f"{self.name} | USER BANNED")
                await self.client.disconnect()
                return False
        await self.client.disconnect()
        tg_web_data = url_decode(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        self.headers["tl-init-data"] = tg_web_data
        self.session.headers["tl-init-data"] = tg_web_data
        return tg_web_data

    async def run(self):
        logger.info(f"Thread {self.thread} | {self.name} | Start!")
        await self.login()
        while True:
            await self.play()
