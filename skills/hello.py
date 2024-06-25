from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('/hello')
def get(message_request: MessageRequest):
    print(MessageRequest)
    return [
        TextSendMessage(text='Hello World!')
    ]