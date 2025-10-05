from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
import random
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
import requests
import time

__plugin_meta__ = PluginMetadata(
    name="mew",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

mew = on_command("喵")

@mew.handle()
async def mew_handle(event: Event):
    id = event.get_user_id()
    time.sleep(2)
    if id == config.admin_id:  # type: ignore
        await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 喵~"))

    elif id == config.friend_id:  # type: ignore
        await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 你好喵~"))

    else:
        t = random.randint(1, 10)
        if t <= 6:
            await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 喵!"))
        elif t <= 9:
            await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 喵喵!"))
        else:
            await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 哈!"))