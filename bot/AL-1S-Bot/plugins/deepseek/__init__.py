from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .config import Config
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam



__plugin_meta__ = PluginMetadata(
    name="deepseek",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

deepseek = on_command("ds")

def get_answer(message: str, mode: str = "normal"):
    client = OpenAI(api_key = config.api_key, base_url="https://api.deepseek.com") # type: ignore
    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": "你是游戏蔚蓝档案中千年科技学院的爱丽丝，是天真可爱的小萝莉，但实际上是个机器人。"}]
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    if mode == "normal":
        return response.choices[0].message.content
    elif mode == "debug":
        return "\n".join(
            [f'{msg["role"]}: {msg["content"]}' for msg in messages] # type: ignore
        )
@deepseek.handle()
async def Answer(event: Event):
    
    user = event.get_message()[0].data["text"][3:]

    if " -debug" in user:
        answer = get_answer(user, mode="debug")
    else:
        answer = get_answer(user, mode="normal")
    
    if answer:
        await deepseek.finish(answer)
    else:
        await deepseek.finish("呜呜呜出bug了呜呜呜")