from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .config import Config
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from . import db
from .tools import short
from time import sleep
__plugin_meta__ = PluginMetadata(
    name="deepseek",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

deepseek = on_command("ds")

db.init_db() #init db

def get_answer(user_message: str, mode: str = "normal", user_id: str = 'unknown'):
    client = OpenAI(api_key = config.api_key, base_url="https://api.deepseek.com") # type: ignore
    #system prompt
    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": config.system_prompt}] # type: ignore

    total_message = f"以下是用户本次的发言\n{db.get_user_message(user_id)}\n \
                      以下是该用户的自我介绍介绍\n{db.get_user_intro(user_id)}\n \
                      以下是你与该用户最近的聊天记录\n{db.get_user_message(user_id)}\n \
                      以下是你与所有用户最近的聊天记录\n{db.get_all_message()}\n \
                      请基于以上信息来回应用户"
    
    messages.append({"role": "user", "content": total_message})
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = messages
    )

    db.save_message(user_id, user_message, response.choices[0].message.content) # type: ignore

    if mode == "normal":
        return response.choices[0].message.content
    elif mode == "debug":
        print(total_message)
        return short(total_message) + "\n\n" + response.choices[0].message.content # type: ignore
    
@deepseek.handle()
async def Answer(event: Event):
    try:
        user_message = event.get_message()[0].data["text"][3:]
        user_id = str(event.get_user_id())

        if " -debug" in user_message:
            if user_id != config.admin_id: # type: ignore
                sleep(1)
                await deepseek.finish("只有Reyar老师可以使用debug模式哦！")
            else:
                answer = get_answer(user_message, mode="debug", user_id=user_id)

        elif "-db" in user_message:
            if user_id != config.admin_id: # type: ignore
                sleep(1)
                await deepseek.finish("只有Reyar老师可以操作数据库哦！")
                
            if "show" in user_message:
                await deepseek.finish(f"database:\n{db.show_db()}")
                answer = None

            elif "clear" in user_message:
                db.clear_db()
                await deepseek.finish("邦邦卡邦！爱丽丝失忆了哦！")
                answer = None     

        elif "-help" in user_message:
            sleep(1)
            await deepseek.finish("输入/ds 后就可以直接跟爱丽丝聊天哦~\n \
                                   如果想要爱丽丝认识你，可以使用\"/ds -register 你的自我介绍\"来告诉爱丽丝你是谁哦~")

        elif "-register" in user_message:
            if "clear" in user_message and user_id == config.admin_id: # type: ignore
                sleep(1)
                id = user_message.replace("/ds -register clear ", "").strip()
                db.cancel_register(id)
                await deepseek.finish(MessageSegment.at(id) + MessageSegment.text(" 什么的，爱丽丝不认识哦"))
            else:
                sleep(1)
                intro = user_message.replace("/ds -register ", "").strip()
                db.register_user(user_id, intro)
                await deepseek.finish(MessageSegment.at(user_id) + MessageSegment.text(" 爱丽丝记住你啦！"))
            answer = None

        else:
            answer = get_answer(user_message, mode="normal", user_id=user_id)
        

        if answer:
            await deepseek.finish(answer)
        else:
            pass
    
    except Exception as e:
        if "Finished" in str(e): #ignore finished
            pass
        else:
            await deepseek.finish(f"呜呜呜出bug了呜呜呜\n{e}")