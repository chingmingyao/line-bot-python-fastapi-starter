from typing import Text
from linebot.models import TextSendMessage
from pyscreeze import locateOnWindow
from models.message_request import MessageRequest
from skills import add_skill
from linebot.models.template import TemplateSendMessage,ButtonsTemplate
from linebot.models.actions import LocationAction   



@add_skill('{action_location}')
def get(message_request: MessageRequest):
    location = TemplateSendMessage(
        alt_text='Actions',
        template=ButtonsTemplate(
    
            title='Menu',
            text='地址選擇器',
            actions=[
               LocationAction(label="地址選擇器1")
            ]
        )
        
    )
    
    return [location]