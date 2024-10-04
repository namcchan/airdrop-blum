# 🚀AUTO FARM FOR BLUM, COINSWEEPER, MOONBIX🚀

## Requirements

> [!WARNING]
> I am not responsible for your account. Please consider the potential risks before using this bot.

## Recommendation before use

# 🔥🔥 PYTHON version must be 3.11 🔥🔥

- Python 3.11 (you can install it [here](https://www.python.org/downloads/release/python-3110/))
- Telegram API_ID and API_HASH (you can get them [here](https://my.telegram.org/auth?to=apps))

## Features

|                      Feature                       | Supported |
| :------------------------------------------------: | :-------: |
|                   Multithreading                   |    ✅     |
|              Proxy binding to session              |    ✅     |
|           Support for pyrogram .session            |    ✅     |
| Auto-register your account with your referral link |    ✅     |
|                     Auto tasks                     |    ✅     |
|                     Auto games                     |    ✅     |

## [Settings]

|            Settings             |                                 Description                                  |
| :-----------------------------: | :--------------------------------------------------------------------------: |
|      **API_ID / API_HASH**      |   Platform data from which to run the Telegram session (default - android)   |
|   **USE_RANDOM_DELAY_IN_RUN**   |                              Name saying itself                              |
|     **RANDOM_DELAY_IN_RUN**     |              Random seconds delay for ^^^ (default is [5, 30])               |
| **RANDOM_DELAY_BETWEEN_CYCLES** |      Random minutes delay between cycles (default is [20, 40, 60, 80])       |
|           **USE_REF**           |         Register accounts with ur referral or not (default - False)          |
|           **REF_ID**            |   Your referral argument (comes after app/startapp? in your referral link)   |
|     **USE_PROXY_FROM_FILE**     | Whether to use a proxy from the `bot/config/proxies.txt` file (True / False) |
|      **ENABLE_AUTO_TASKS**      |                       Enable auto tasks (True / False)                       |
|   **ENABLE_AUTO_PLAY_GAMES**    |                    Enable auto play games (True / False)                     |
|       **MAX_GAME_POINTS**       |           Maximum available points per one game (Recommended 200)            |

## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

1. Install the required dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Get your API_ID and API_HASH:

   - Go to [my.telegram.org](https://my.telegram.org/auth?to=apps)
   - Sign in with your Telegram account
   - Create a new application to get your API_ID and API_HASH

3. Configure the application:

   - Open `config.py` and add your `API_ID` and `API_HASH`:

     ```python
     API_ID = your_api_id
     API_HASH = 'your_api_hash'
     ```

   - If you want to use a proxy, set `USE_PROXY` in `config.py` to `True`, otherwise set it to `False`:

     ```python
     USE_PROXY = True  # or False
     ```

   - If `USE_PROXY` is `True`, open `proxy.txt` and fill it out using the example provided. Ensure there are no extra lines in the file.
     Proxy format : ip:port:login:password session_name, session name is which use this proxy (WITHOUT .session, only session name)

   ```txt
   192.168.1.1:1234:username:password
   192.168.1.2:2934:username:password
   192.168.1.3:3834:username:password
   192.168.5.1:2884:username:password
   ```

   And don't forget set proxy type in `config.py`

   ```python
   PROXY_TYPE = "socks5" # or http
   ```

4. IMPORTANT Create a `sessions` folder

## Usage

1. Run the bot:

   ```bash
   python main.py
   ```

2. The software will work with all accounts using the single `API_ID` and `API_HASH`. No need to change them for each account.

## Important Notes

- **Python Version:** The software runs on Python 3.11. Using a different version may cause errors.
- DONT USE MAIN ACCOUNT BECAUSE THERE IS ALWAYS A CHANCE TO GET BANNED IN TELEGRAM
