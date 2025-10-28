from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
import subprocess
import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event

__plugin_meta__ = PluginMetadata(
    name="BiliDown",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

download = on_command("Download")

@download.handle()
async def download_handle(event: Event):
    id = event.get_user_id()
    url = str(event.get_message()).strip()
    await download.send(MessageSegment.at(id) + MessageSegment.text("视频开始下载..."))
    bvid = url.split("bilibili.com/video/")[1].split("?")[0].split("/")[0]
    cmd = ["BBDown", url, "--work-dir /root/Video/", bvid]
    process = await subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        video_path = os.path.join("/root/Video/", bvid + ".mp4")
        if os.path.exists(video_path):
            await download.send(MessageSegment.at(id) + MessageSegment.video(video_path))
        else:
            await download.finish(MessageSegment.at(id) + MessageSegment.text("视频文件未找到!"))
    else:
        await download.finish(MessageSegment.at(id) + MessageSegment.text("视频下载失败! 错误信息: " + stderr.decode()))

