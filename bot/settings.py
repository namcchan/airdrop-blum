from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    WORKDIR: str = "sessions/"
    API_ID: int
    API_HASH: str

    USE_TG_BOT: bool = False
    BOT_TOKEN: str
    CHAT_ID: str

    USE_PROXY : bool = True
    PROXY_TYPE: str = "socks5"

    ACC_DELAY: list[int] = [5, 15]
    POINTS : list[int] = [240, 250]
    SPEND_DIAMONDS : bool = True
    DO_TASKS : bool = True
    SLEEP_GAME_TIME : list[int] = [30,50]
    MINI_SLEEP : list[int] = [3,7]
    SLEEP_8HOURS : list[int] = [60*60, 120*60]

    COINSWEEPER_GAME_PLAY_EACH_ROUND: list[int] = [2, 4]
    COINSWEEPER_TIME_PLAY_EACH_GAME: list[int] = [30, 60]
    COINSWEEPER_DELAY_EACH_ACCOUNT: list[int] = [20, 30]


settings = Settings()
