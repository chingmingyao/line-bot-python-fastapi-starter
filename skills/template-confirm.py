from typing import Text
from linebot.models.template import ConfirmTemplate
from linebot.models import  TemplateSendMessage
from linebot.models.actions import MessageAction
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('{confirm}')
def get(message_request: MessageRequest):
    Confirm_template_message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='Are you sure',
        actions=[
                MessageAction(
                        label='Yes',
                        text='You Said:YES'
                ),
                MessageAction(
                        label='NO',
                        text='You Said:No'
                )
    ]
)
)

    
    
    return [
        Confirm_template_message
    ]