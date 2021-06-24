from sys import platform
from typing import Union

from scrapli import AsyncScrapli
from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver

from app.config import get_settings, Settings

settings: Settings = get_settings()


class Host():
    def __init__(self, hostname: str, ip: str, platform: str):
        self.hostname: str = hostname
        self.ip: str = ip
        self.platform: str = platform
        self.con: Union[AsyncIOSXEDriver, AsyncNXOSDriver] = None

    async def get_con(self):
        if not self.con :
            self.con = AsyncScrapli(
                host = self.ip,
                auth_username = settings.API_USER,
                auth_password = settings.API_PASSWORD,
                auth_secondary = settings.API_PASSWORD,
                auth_strict_key = False,
                platform = self.platform,
                transport = "asyncssh"
            )
            self.con.open()
        return self.con        
