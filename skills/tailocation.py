import re,json,os,pyproj,math,trans_map
from typing import Text
from linebot.models import FlexSendMessage
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
    
def tai_to_loc(tai):
    
    lat, lon = trans_map.tai_to_wgs(tai)
    return lat, lon




@add_skill('/台電')
def get(message_request: MessageRequest):
    
    msg_array = message_request.message.split()
    tai= msg_array[1]
    result = tai_to_loc(tai)
    msg2 =(f"https://maps.nlsc.gov.tw/T09/mapshow.action?language=ZH&lat={result[0]}&lon={result[1]}&zoom=18") 
    
    
  
    
    try:
        flex = json.load(open(os.path.join(os.getcwd(), 'skills', 'tailocation.json'), 'r', encoding='utf-8'))
        
        flex['body']['contents'][1]['contents'][0]['contents'][0]['text'] = f'台電座標： {tai}'
        flex['body']['contents'][1]['contents'][1]['contents'][0]['text'] = f'經緯度  ： {result[0]},{result[1]}'
        
        
        print(f'經緯度 {result[0]},{result[1]}')
        flex['footer']['contents'][0]['action']['uri'] = f'https://www.google.com.tw/maps/place/{result[0]},{result[1]}'
        print(f"google https://www.google.com.tw/maps/place/{result[0]},{result[1]}")
        flex['footer']['contents'][1]['action']['uri'] = (f"https://maps.nlsc.gov.tw/T09/mapshow.action?language=ZH&lat={result[0]}&lon={result[1]}&zoom=18") 
        msg1 =FlexSendMessage(alt_text="1",contents=flex)
        return [
           msg1
        ]       
        
    except Exception as e:
        print(f"Error loading JSON: {e}")
        msg = TextSendMessage(text=f"Error loading JSON: {e}")
        msg1= TextSendMessage(os.path.join(os.getcwd(), 'skills', 'tailocation.json'))
        return [
           msg1
        ]
    

            
           