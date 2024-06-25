from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('{sticker}')
def get(message_request: MessageRequest):
    
    
    txt = '$ LINE emoji $'
    emoji = [
        {
            "index": 0,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "001"
        },
        {
            "index": 13,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "002"
        }
    ]
    
    return [
        TextSendMessage(text=f'You said: {message_request.message}')
    ]