import cv2
import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_padlocal_1320c819baf548c4a20f394443422b70'
os.environ['WECHATY_PUPPET']='wechaty-puppet-service'
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'puppet_padlocal_1320c819baf548c4a20f394443422b70'
import asyncio
import logging
from typing import Optional, Union
from wechaty_puppet import FileBox, ScanStatus  # type: ignore
import paddlex as pdx

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
model = pdx.load_model('best_model')

def Pokemon_Identify(img_name, img_path):

    # 模型预测
    result = model.predict(img_path, topk=3)

    return result




class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    step = 0
    def __init__(self):
        super().__init__()

        # 图像信息
        # [flag, img, img_name, img_path, img_new_name, img_new_path]
        self.img = [True, None, None, None, None, None]
    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        global state
        from_contact = msg.talker()
        text = msg.text()
        type = msg.type()
        room = msg.room()
        # 不处理群消息
        if room is None:
            if text == 'hi' or text == '你好':
                conversation = from_contact
                await conversation.ready()
                await conversation.say(
                    '这是自动回复：机器人目前的功能有：识别宝可梦\n 请您输入一张宝可梦的图片')
                state=100

            if text == 'ding':
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：dong dong dong')

            if text == 'Pikachu':
                conversation = from_contact

                # 从网络上加载图片到file_box
                img_url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg15.3lian.com%2F2015%2Ff2%2F103%2Fd%2F63.jpg&refer=http%3A%2F%2Fimg15.3lian.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1632844162&t=6e6e3a15b0d802b2d3c5c4ebe21cab85'
                file_box = FileBox.from_url(img_url, name='xx.jpg')
                await conversation.ready()
                await conversation.say('这是自动回复：')
                await conversation.say(file_box)

            # 如果消息类型是图片
            if state == 100 and type == Message.Type.MESSAGE_TYPE_IMAGE:
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：正在飞速识别中...')

                # 将msg转换为file_box
                file_box = await msg.to_file_box()

                # 获取图片名
                img_name = file_box.name

                # 图片保存的路径
                img_path = './images/' + img_name

                # 将图片保存到文件中
                await file_box.to_file(file_path=img_path, overwrite=True)

                # 调用函数，获取图片新路径
                result = Pokemon_Identify(img_name, img_path)
                a = str(result[0])
                state=a[16]
                await conversation.say(a)
            if state=='0':
                state=0
                conversation=from_contact
                await conversation.ready()
                await conversation.say('它是妙蛙种子\n基本资料:https://wiki.52poke.com/wiki/%E5%A6%99%E8%9B%99%E7%A7%8D%E5%AD%90')
            if state=='1':
                state=0
                conversation=from_contact
                await conversation.ready()
                await conversation.say('它是小火龙\n基本资料：https://wiki.52poke.com/zh-hans/%E5%B0%8F%E7%81%AB%E9%BE%99')
            if state=='2':
                state=0
                conversation=from_contact
                await conversation.ready()
                await conversation.say('它是超梦\n基本资料：https://wiki.52poke.com/wiki/%E8%B6%85%E6%A2%A6')
            if state=='3':
                state=0
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这只是皮卡丘\n基本资料：http://www.pokemon.name/wiki/%E7%9A%AE%E5%8D%A1%E4%B8%98#.E5.9F.BA.E6.9C.AC.E8.B5.84.E6.96.99')
            if state=='4':
                state=0
                conversation=from_contact
                await conversation.ready()
                await conversation.say('这只是杰尼龟\n基本资料：https://wiki.52poke.com/zh-hans/%E6%9D%B0%E5%B0%BC%E9%BE%9F')


    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())