from typing import Text
from linebot.models import TextSendMessage,TextMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('{text}')
def get(message_request: MessageRequest):
    msg = TextMessage(text='Hello')
    
    txt = '$ LINE emoji $'
    emoji = [
        {
            "index": 0,   #0表示第1個$的位並指定要什麼emoji
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "001"
        },
        {
            "index": 13,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "002"
        }
    ]
    print(txt.find('$',1)) #find first $ positon
    return [TextSendMessage(text=txt,emojis=emoji)]
    
    