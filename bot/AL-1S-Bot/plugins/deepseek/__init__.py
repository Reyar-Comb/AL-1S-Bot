from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .config import Config
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from . import db
from .tools import short

__plugin_meta__ = PluginMetadata(
    name="deepseek",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

deepseek = on_command("ds")

db.init_db() #init db

def get_answer(message: str, mode: str = "normal", user_id: str = 'unknown'):
    client = OpenAI(api_key = config.api_key, base_url="https://api.deepseek.com") # type: ignore
    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": config.system_prompt}] # type: ignore

    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    db.save_message(user_id, message, response.choices[0].message.content) # type: ignore

    if mode == "normal":
        return response.choices[0].message.content
    elif mode == "debug":
        return "\n".join(
            [f'{msg["role"]}: {short(msg["content"])}' for msg in messages] # type: ignore
        )
    
@deepseek.handle()
async def Answer(event: Event):
    try:
        user_message = event.get_message()[0].data["text"][3:]
        user_id = str(event.get_user_id())

        if " -debug" in user_message:
            answer = get_answer(user_message, mode="debug", user_id=user_id)

        elif "-db show" in user_message:
            await deepseek.finish(f"database:\n{db.show_db()}")
            answer = None

        elif "-db clear" in user_message:
            db.clear_db()
            await deepseek.finish("邦邦卡邦！爱丽丝失忆了哦！")
            answer = None     

        else:
            answer = get_answer(user_message, mode="normal")
        

        if answer:
            await deepseek.finish(answer)
        else:
            pass
    
    except Exception as e:
        if "Finished" in str(e): #ignore finished
            pass
        else:
            await deepseek.finish(f"呜呜呜出bug了呜呜呜\n{e}")