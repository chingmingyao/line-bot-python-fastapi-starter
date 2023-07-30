import os
import re
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.params import Header
from starlette.requests import Request
from models.message_request import MessageRequest
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage,TextMessage
from skills import *
from skills import skills
from pathlib import Path
from linebot.models.messages import ImageMessage, FileMessage,LocationMessage

app = FastAPI()

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

def get_message(request: MessageRequest):
    for pattern, skill in skills.items():
        if re.match(pattern, request.intent):
            return skill(request)
    request.intent = '{not_match}'
    return skills['{not_match}'](request)

@app.post("/api/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")
    return 'OK'
    
@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    msg_request = MessageRequest()
    msg_request.intent = event.message.text
    msg_request.message = event.message.text
    msg_request.user_id = event.source.user_id
    
    func = get_message(msg_request)
    line_bot_api.reply_message(event.reply_token, func)

@handler.add(event=MessageEvent, message=ImageMessage)
def handle_message(event):
    print('image', event)
    #���o�T��ID
    message_id = event.message.id
    print(message_id)
    #�z�T��ID���o�������@�����������W���Ϥ�
    message_content = line_bot_api.get_message_content(message_id)
    #�N�Ϥ��s����A���W
    with open(Path(f'images/{message_id}.jpg').absolute(),"wb") as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

@handler.add(event=MessageEvent, message=LocationMessage)
def handle_message(event):
    print('location', event)
    print('-----')
    print(event.message.latitude)
    print(event.message.longitude)


# @handler.add(event=MessageEvent, message=FileMessage)
# def handle_message(event):
#     print('file', event)
#     static_tmp_path = os.path.join(os.path.dirname(__file__), 'files')
#     message_content = line_bot_api.get_message_content(event.message.id)
#     with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
#         for chunk in message_content.iter_content():
#             tf.write(chunk)
#         tempfile_path = tf.name

#     dist_path = tempfile_path + '-' + event.message.file_name
#     dist_name = os.path.basename(dist_path)
#     os.rename(tempfile_path, dist_path)
