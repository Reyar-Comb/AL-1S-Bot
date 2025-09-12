from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .config import Config
import time

__plugin_meta__ = PluginMetadata(
    name="gif",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

getGIF = on_command("gif")

@getGIF.got("gif", prompt = "可以发表情给爱丽丝了哦~")
async def get_gif(event: Event):
    a = event.get_message()[0]
    if a.type != "image":
        time.sleep(1)
        await getGIF.finish("主人发的好像不是表情呢qwq")
    else:
        time.sleep(1)
        url = a.data["url"]
        await getGIF.finish("点开链接就能下载GIF啦!\n" + url)
