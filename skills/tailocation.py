import re,json,os
from typing import Text
from linebot.models import FlexSendMessage
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('/台電')
def get(message_request: MessageRequest):
    
    msg_array = message_request.message.split()
    tai= msg_array[1]
    result = tai_to_loc(tai)
    
    flex = json.load(open(os.getcwd()+
                          '\\skills\\' 'tailocation.json','r',encoding='utf-8'))
    flex['body']['contents'][1]['text'] = f'台電座標 {tai}'
    flex['body']['contents'][3]['text'] = f'經緯度 {result[0]},{result[1]}'
    print(f'經緯度 {result[0]},{result[1]}')
    flex['footer']['contents'][0]['action']['uri'] = f'https://www.google.com.tw/maps/place/{result[0]},{result[1]}'
    print(f"google https://www.google.com.tw/maps/place/{result[0]},{result[1]}")
  
   
   
    msg = FlexSendMessage(alt_text='座標轉換',contents=flex)
    
    return [
        msg
    ]
    
def tai_to_loc(tai):
    
    import trans_map
    lat, lon = trans_map.tai_to_wgs(tai)
    return lat, lon