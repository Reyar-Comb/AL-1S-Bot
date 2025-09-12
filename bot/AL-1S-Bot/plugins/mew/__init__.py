from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

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
    time.sleep(1)
    if id == "2290197845":
        await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 喵~"))
    else:
        await mew.finish(MessageSegment.at(id) + MessageSegment.text(" 哈!"))