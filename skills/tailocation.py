import re,json,os,pyproj,math
from typing import Text
from linebot.models import FlexSendMessage
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
    
def tai_to_loc(tai):
    import trans_map
    lat, lon = trans_map.tai_to_wgs(tai)
    return lat, lon

# TWD97 = pyproj.Proj(3826) #定義TWD97坐標系 121分帶
# TWD67 = pyproj.Proj(3828) #定義TWD67坐標系EPSG:3828
# WGS84 = pyproj.Proj(4326)



# ooc_G ={'A':[170000,2750000],'B':[250000,2750000],'C':[330000,2750000],'D':[170000,1700000],
#       'E':[250000,2700000],'F':[330000,2700000],'G':[170000,2650000],'H':[250000,2650000],
#       'J':[90000,2600000],'K':[170000,2600000],'L':[250000,2600000],'M':[90000,2550000],
#       'N':[170000,2550000],'O':[250000,2550000],'P':[90000,2500000],'Q':[170000,2500000],
#       'R':[250000,2500000]} #origin_of_coordinates

# ooc_RS ={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8}

# #臺電座標轉換為WGS84
# def tai_to_wgs(tai_loc:str)->tuple:
#     """
#     輸入台電座標 範例:G3320CB52 回傳元組(24.123456,120.123456)
#     """
#     tai_loc = tai_loc.upper()
#     if len(tai_loc) < 11:
#         loc_X = ooc_G[tai_loc[0]][0]+800*int(tai_loc[1:3])+100*int(ooc_RS[tai_loc[5:6]]-1)+10*int(tai_loc[7:8])
#         loc_Y = ooc_G[tai_loc[0]][1]+500*int(tai_loc[3:5])+100*int(ooc_RS[tai_loc[6:7]]-1)+10*int(tai_loc[8:9])
#     else:
#         #twd67
#         loc_X = ooc_G[tai_loc[0]][0]+800*int(tai_loc[1:3])+100*(ooc_RS[tai_loc[5:6]]-1)+10*int(tai_loc[7:8])+int(tai_loc[9:10])
#         loc_Y = ooc_G[tai_loc[0]][1]+500*int(tai_loc[3:5])+100*(ooc_RS[tai_loc[6:7]]-1)+10*int(tai_loc[8:9])+int(tai_loc[10:11])
# #     print(f'TWD67:{loc_X},{loc_Y}')
#     global lat,lon
#     lat,lon = pyproj.transform(TWD97, WGS84,loc_X+828,loc_Y-207) #TWD97 轉換為WGS84 121分帶
# #     print(f'WGS84:{lon},{lat}')
#     lat = str(lat)[:9]
#     lon = str(lon)[:10]
#     return lat,lon

# def taipower_loc(lon:int,lat:int)->str:
#     """
#      輸入Google 座標 lon:120.506112, lat:23.970121 
#      轉換成台電座標  G3604BA0008
#     """    
#     lon,lat = TWD97(lon,lat)
# #     lon,lat = TWD97(120.506112, 23.970121) #G3604BA0008
    

#     #TWD97->TWD67
#     lon = int(lon)-828
#     lat = int(lat)+207

#     global tai_block

#     #判斷區塊
#     if lon >= 170000 and lon < 250000 and lat >= 2750000 and lat < 2800000:
#         tai_block ='A'
#     elif lon >= 250000 and lon < 330000 and lat >= 2750000 and lat < 2800000:
#         tai_block = 'B'
#     elif lon >= 330000 and lon < 410000 and lat >= 2750000 and lat < 2800000:
#         tai_block = 'C'
#     elif lon >= 170000 and lon < 250000 and lat >= 2700000 and lat < 2750000:
#         tai_block = 'D'
#     elif lon >= 250000 and lon < 330000 and lat >= 2700000 and lat < 2750000:
#         tai_block = 'E'
#     elif lon >= 330000 and lon < 410000 and lat >= 2700000 and lat < 2750000:
#         tai_block = 'F'
# #     elif lon >= 170000 and lon < 250000 and lat >= 2650000 and lat < 2700000:
#     elif 170000 <= lon < 250000 and 2650000 <= lat < 2700000:
#         tai_block = 'G'
#     elif lon >= 250000 and lon < 330000 and lat >= 2650000 and lat < 2700000:
#         tai_block = 'H'
#     elif lon >= 90000 and lon < 170000 and lat >= 2600000 and lat < 2650000:
#         tai_block = 'J'
#     elif lon >= 170000 and lon < 250000 and lat >= 2600000 and lat < 2650000:
#         tai_block = 'K'
#     elif lon >= 250000 and lon < 330000 and lat >= 2500000 and lat < 2550000:
#         tai_block = 'R'
#     elif lon >= 250000 and lon < 330000 and lat >= 2600000 and lat < 2650000:
#         tai_block = 'L'
#     elif lon >= 90000 and lon < 170000 and lat >= 2550000 and lat < 2600000:
#         tai_block = 'M'
#     elif lon >= 170000 and lon < 250000 and lat >= 2550000 and lat < 2600000:
#         tai_block = 'N'
#     elif lon >= 250000 and lon < 330000 and lat >= 2550000 and lat < 2600000:
#         tai_block = 'O'
#     elif lon >= 250000 and lon < 330000 and lat >= 2500000 and lat < 2550000:
#         tai_block = 'P'
#     elif lon >= 170000 and lon < 250000 and lat >= 2500000 and lat < 2550000:
#         tai_block = 'Q'

#     tai_PP = int(round((lon - ooc_G[tai_block][0])/800,2))
#     tai_QQ = int(round((lat - ooc_G[tai_block][1])/500,2))
#     tai_R = math.floor(((lon-ooc_G[tai_block][0])%800)/100)
#     tai_S = math.floor(((lat-ooc_G[tai_block][1])%500)/100)
#     tai_T = math.floor(((lon-ooc_G[tai_block][0])%800)%100/10)
#     tai_U = math.floor(((lat-ooc_G[tai_block][1])%500)%100/10)
#     tai_V = str(lon)[-1]
#     tai_W = str(lat)[-1]

#     # #RS 轉換
#     tai_R = int(tai_R)
#     tai_RS = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
#     new_tai_R = list (tai_RS.keys()) [list (tai_RS.values()).index (tai_R)]
#     new_tai_S = list (tai_RS.keys()) [list (tai_RS.values()).index (tai_S)]
#     new_tai_S

#     #台電座標
#     tai_PP = str(tai_PP)
#     tai_QQ = str(tai_QQ)

#     if len(tai_PP) ==1:
#         tai_PP = "0" + tai_PP
#     if len(tai_QQ) ==1:
#         tai_QQ = '0' + tai_QQ


#     global taipowerloc
   
#     global taipowerloc_dic
#     taipowerloc_dic ={'G':tai_block,'PP':tai_PP,'QQ':tai_QQ,'R':new_tai_R,'S':new_tai_S,'T':tai_T,'U':tai_U,'V':tai_V,'W':tai_W}
#     taipowerloc = tai_block + tai_PP + tai_QQ + new_tai_R + new_tai_S + str(tai_T) + str(tai_U) + str(tai_U) + str(tai_W)
#     return taipowerloc

@add_skill('/台電')
def get(message_request: MessageRequest):
    
    msg_array = message_request.message.split()
    tai= msg_array[1]
    result = tai_to_loc(tai)
    
    
    
  
    
    try:
        flex = json.load(open(os.path.join(os.getcwd(), 'skills', 'tailocation.json'), 'r', encoding='utf-8'))
        flex['body']['contents'][1]['text'] = f'台電座標 {tai}'
        flex['body']['contents'][3]['text'] = f'經緯度 {result[0]},{result[1]}'
        print(f'經緯度 {result[0]},{result[1]}')
        flex['footer']['contents'][0]['action']['uri'] = f'https://www.google.com.tw/maps/place/{result[0]},{result[1]}'
        print(f"google https://www.google.com.tw/maps/place/{result[0]},{result[1]}")
        msg2 = FlexSendMessage(alt_text='匯率轉換',contents=flex)
        msg1 = TextSendMessage(os.path.join(os.getcwd(), 'skills', 'tailocation.json'))
        return [
        msg2,msg1]
        
    except Exception as e:
        print(f"Error loading JSON: {e}")
        msg = TextSendMessage(text=f"Error loading JSON: {e}")
        return [
            msg
        ]
    
    