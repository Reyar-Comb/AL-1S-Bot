from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .config import Config
from openai import OpenAI




__plugin_meta__ = PluginMetadata(
    name="deepseek",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

deepseek = on_command("ds")

@deepseek.handle()
async def Answer(event: Event):
    client = OpenAI(api_key = config.api_key, base_url="https://api.deepseek.com") # type: ignore
    messages = [{"role": "system", "content": "你是游戏蔚蓝档案中千年科技学院的爱丽丝，是天真可爱的小萝莉，但实际上是个机器人。"}]
    user = event.get_message()[0].data["text"][3:]
    await deepseek.finish("user: " + user)