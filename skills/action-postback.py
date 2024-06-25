from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
from linebot.models.template import TemplateSendMessage,ButtonsTemplate
from linebot.models.actions import PostbackAction


@add_skill('{action_postback}')
def get(message_request: MessageRequest):
    
    msg = TemplateSendMessage(
    alt_text='Actions',
    template=ButtonsTemplate(
        title='Menu',
        text='Please Click',
        actions=[
            PostbackAction(label="test11", data="345345345")
            ]
        )
    )   
    return [
       msg
    ]