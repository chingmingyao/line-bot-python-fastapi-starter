from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
from linebot.models import TemplateSendMessage
from linebot.models.actions import MessageAction
from linebot.models.template import ButtonsTemplate


@add_skill('{action_message}')
def get(message_request: MessageRequest):
    
    
    msg = TemplateSendMessage(
    alt_text='Actions',
    template=ButtonsTemplate(
        title='Menu',
        text='Please Click',
        actions=[
            MessageAction(
                label='點我目貼圖',
                text='{sticker}'
                )
            ]
        )
    )
    return [
        msg
    ]