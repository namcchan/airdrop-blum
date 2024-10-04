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

    BLUM_DELAY: list[int] = [5, 15]
    BLUM_POINTS : list[int] = [240, 250]
    BLUM_SPEND_DIAMONDS : bool = True
    BLUM_DO_TASKS : bool = True
    BLUM_SLEEP_GAME_TIME : list[int] = [30,50]
    BLUM_MINI_SLEEP : list[int] = [3,7]
    BLUM_SLEEP_8HOURS : list[int] = [60*60, 120*60]

    COINSWEEPER_GAME_PLAY_EACH_ROUND: list[int] = [2, 4]
    COINSWEEPER_TIME_PLAY_EACH_GAME: list[int] = [30, 60]
    COINSWEEPER_DELAY_EACH_ACCOUNT: list[int] = [20, 30]
    COINSWEEPER_REF_CODE: str = "6624523270"

    MOONBIX_RUNNING_DELAY: list[int] = [5, 40]
    MOONBIX_DELAY_BEETWEN_CYLCES: list[int] = [20, 40, 60, 80]
    MOONBIX_MAX_GAME_POINT: int = 300
    MOONBIX_AUTO_PLAY_GAME: bool = True
    MOONBIX_AUTO_TAKS: bool = True

settings = Settings()
