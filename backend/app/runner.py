from typing import *

from net_gsd import Runner

from app.config import Settings, get_settings

settings: Settings = get_settings()


def get_runner(hosts: List[dict] = None) -> Runner:
    return Runner(username=settings.API_USER, password=settings.API_PASSWORD, hosts=hosts)
