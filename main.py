# -*- coding: utf-8 -*-
import os,re,sqlite3
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
import uvicorn
 
 
app = FastAPI()

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


# DATABASE = 'test.db'
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# def create_tables():
#     conn = get_db_connection()
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS messages (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id TEXT NOT NULL,
#             message TEXT NOT NULL,
#             intent TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()




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
    
    
        # Save message to the database
    # conn = get_db_connection()
    # conn.execute(
    #     "INSERT INTO messages (user_id, message, intent) VALUES (?, ?, ?)",
    #     (msg_request.user_id, msg_request.message, msg_request.intent)
    # )
    # conn.commit()
    # conn.close()

    func = get_message(msg_request)
    line_bot_api.reply_message(event.reply_token, func)

@handler.add(event=MessageEvent, message=ImageMessage)
def handle_message(event):
    print('image', event)
    #取得訊息ID
    message_id = event.message.id
    print(message_id)
    #透訊息ID取得ｌｉｎｅ　ｓｅｒｖｅｒ上的圖片
    message_content = line_bot_api.get_message_content(message_id)
    #將圖片存到伺服器上
    with open(Path(f'images/{message_id}.jpg').absolute(),"wb") as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

@handler.add(event=MessageEvent, message=LocationMessage)
def handle_message(event):
    print('location', event)
    print('-----')
    print(event.message.latitude)
    print(event.message.longitude)

if __name__ == "__main__":
   
    uvicorn.run(app, host="0.0.0.0", port=8000) 

