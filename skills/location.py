from typing import Text
from linebot.models import LocationMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('{/location}')
def get(message_request: MessageRequest):
    msg =LocationMessage('臺北101',address ='信義路',latitude=25.033843,longitude=121.564)
    
    return [ 
            msg
    ]
  
    
#     @handler.add(event=MessageEvent, message=LocationMessage)
# def handle_message(event):
#     print('location',event)
#     print("---------------------")
#     print(event.message.latitude)
#     print(event.message.longitude)