import pyproj,math,webbrowser,time


TWD97 = pyproj.Proj(3826) #定義TWD97坐標系 121分帶
TWD67 = pyproj.Proj(3828) #定義TWD67坐標系EPSG:3828
WGS84 = pyproj.Proj(4326)



ooc_G ={'A':[170000,2750000],'B':[250000,2750000],'C':[330000,2750000],'D':[170000,1700000],
      'E':[250000,2700000],'F':[330000,2700000],'G':[170000,2650000],'H':[250000,2650000],
      'J':[90000,2600000],'K':[170000,2600000],'L':[250000,2600000],'M':[90000,2550000],
      'N':[170000,2550000],'O':[250000,2550000],'P':[90000,2500000],'Q':[170000,2500000],
      'R':[250000,2500000]} #origin_of_coordinates

ooc_RS ={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8}

#臺電座標轉換為WGS84
def tai_to_wgs(tai_loc:str)->tuple:
    """
    輸入台電座標 範例:G3320CB52 回傳元組(24.123456,120.123456)
    """
    tai_loc = tai_loc.upper()
    if len(tai_loc) < 11:
        loc_X = ooc_G[tai_loc[0]][0]+800*int(tai_loc[1:3])+100*int(ooc_RS[tai_loc[5:6]]-1)+10*int(tai_loc[7:8])
        loc_Y = ooc_G[tai_loc[0]][1]+500*int(tai_loc[3:5])+100*int(ooc_RS[tai_loc[6:7]]-1)+10*int(tai_loc[8:9])
    else:
        #twd67
        loc_X = ooc_G[tai_loc[0]][0]+800*int(tai_loc[1:3])+100*(ooc_RS[tai_loc[5:6]]-1)+10*int(tai_loc[7:8])+int(tai_loc[9:10])
        loc_Y = ooc_G[tai_loc[0]][1]+500*int(tai_loc[3:5])+100*(ooc_RS[tai_loc[6:7]]-1)+10*int(tai_loc[8:9])+int(tai_loc[10:11])
#     print(f'TWD67:{loc_X},{loc_Y}')
    global lat,lon
    lat,lon = pyproj.transform(TWD97, WGS84,loc_X+828,loc_Y-207) #TWD97 轉換為WGS84 121分帶
#     print(f'WGS84:{lon},{lat}')
    lat = str(lat)[:9]
    lon = str(lon)[:10]
    return lat,lon

def taipower_loc(lon:int,lat:int)->str:
    """
     輸入Google 座標 lon:120.506112, lat:23.970121 
     轉換成台電座標  G3604BA0008
    """    
    lon,lat = TWD97(lon,lat)
#     lon,lat = TWD97(120.506112, 23.970121) #G3604BA0008
    

    #TWD97->TWD67
    lon = int(lon)-828
    lat = int(lat)+207

    global tai_block

    #判斷區塊
    if lon >= 170000 and lon < 250000 and lat >= 2750000 and lat < 2800000:
        tai_block ='A'
    elif lon >= 250000 and lon < 330000 and lat >= 2750000 and lat < 2800000:
        tai_block = 'B'
    elif lon >= 330000 and lon < 410000 and lat >= 2750000 and lat < 2800000:
        tai_block = 'C'
    elif lon >= 170000 and lon < 250000 and lat >= 2700000 and lat < 2750000:
        tai_block = 'D'
    elif lon >= 250000 and lon < 330000 and lat >= 2700000 and lat < 2750000:
        tai_block = 'E'
    elif lon >= 330000 and lon < 410000 and lat >= 2700000 and lat < 2750000:
        tai_block = 'F'
#     elif lon >= 170000 and lon < 250000 and lat >= 2650000 and lat < 2700000:
    elif 170000 <= lon < 250000 and 2650000 <= lat < 2700000:
        tai_block = 'G'
    elif lon >= 250000 and lon < 330000 and lat >= 2650000 and lat < 2700000:
        tai_block = 'H'
    elif lon >= 90000 and lon < 170000 and lat >= 2600000 and lat < 2650000:
        tai_block = 'J'
    elif lon >= 170000 and lon < 250000 and lat >= 2600000 and lat < 2650000:
        tai_block = 'K'
    elif lon >= 250000 and lon < 330000 and lat >= 2500000 and lat < 2550000:
        tai_block = 'R'
    elif lon >= 250000 and lon < 330000 and lat >= 2600000 and lat < 2650000:
        tai_block = 'L'
    elif lon >= 90000 and lon < 170000 and lat >= 2550000 and lat < 2600000:
        tai_block = 'M'
    elif lon >= 170000 and lon < 250000 and lat >= 2550000 and lat < 2600000:
        tai_block = 'N'
    elif lon >= 250000 and lon < 330000 and lat >= 2550000 and lat < 2600000:
        tai_block = 'O'
    elif lon >= 250000 and lon < 330000 and lat >= 2500000 and lat < 2550000:
        tai_block = 'P'
    elif lon >= 170000 and lon < 250000 and lat >= 2500000 and lat < 2550000:
        tai_block = 'Q'

    tai_PP = int(round((lon - ooc_G[tai_block][0])/800,2))
    tai_QQ = int(round((lat - ooc_G[tai_block][1])/500,2))
    tai_R = math.floor(((lon-ooc_G[tai_block][0])%800)/100)
    tai_S = math.floor(((lat-ooc_G[tai_block][1])%500)/100)
    tai_T = math.floor(((lon-ooc_G[tai_block][0])%800)%100/10)
    tai_U = math.floor(((lat-ooc_G[tai_block][1])%500)%100/10)
    tai_V = str(lon)[-1]
    tai_W = str(lat)[-1]

    # #RS 轉換
    tai_R = int(tai_R)
    tai_RS = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    new_tai_R = list (tai_RS.keys()) [list (tai_RS.values()).index (tai_R)]
    new_tai_S = list (tai_RS.keys()) [list (tai_RS.values()).index (tai_S)]
    new_tai_S

    #台電座標
    tai_PP = str(tai_PP)
    tai_QQ = str(tai_QQ)

    if len(tai_PP) ==1:
        tai_PP = "0" + tai_PP
    if len(tai_QQ) ==1:
        tai_QQ = '0' + tai_QQ

#     print(f'tai_block:{tai_block} , tai_PP: {tai_PP} , tai_QQ: {tai_QQ} , tai_R: {tai_R}, tai_S: {tai_S} ,tai_T: {tai_T} ,tai_U: {tai_U} ,tai_V: {tai_V} \
#     ,tai_W: {tai_W} \n lon:{lon} ,lat:{lat} , ooc_G : {ooc_G[tai_block]}' )
    global taipowerloc
   
    global taipowerloc_dic
    taipowerloc_dic ={'G':tai_block,'PP':tai_PP,'QQ':tai_QQ,'R':new_tai_R,'S':new_tai_S,'T':tai_T,'U':tai_U,'V':tai_V,'W':tai_W}
    taipowerloc = tai_block + tai_PP + tai_QQ + new_tai_R + new_tai_S + str(tai_T) + str(tai_U) + str(tai_U) + str(tai_W)
    return taipowerloc


# #台電座標->WGS84座標
# def tai_to_loc():
    
#     var = e1.get()
# #     pdb.set_trace()
#     if not (var[0].isalpha() and var[5:7].isalpha() and var[1:5].isdigit() and var[7:9].isdigit()):
#         tk.messagebox.showinfo('錯誤','座標有誤請重新輸入 \n\n 範例:G2800BC31')
#         e1.delete(0,'end')
#     var = var.upper()
    
#     lon,lat = tai_to_wgs(var)
#     e1.delete(0,'end')
#     e1.insert('end',var)
#     e2.delete(0,'end')
#     e2.insert('end',lon + ',' + lat)
#     e3.delete(0,'end')
#     e3.insert('end',lon + ',' + lat)
    
# def loc_to_tai():
#     var = e2.get()
    
#     if str(var).startswith('23') : # lon:121.493772,lat:24.954033
#         lon = str(var[0:9])
#         lat = str(var[10:20])
#         lon,lat = lat,lon
#     else:
#         lon = str(var[0:9])
#         lat = str(var[11:19])
#     print(f'lon:{lon},lat:{lat}')
# #     taipower_loc(lon,lat)
#     taipower_loc(lon,lat)
#     e1.delete(0,'end')
#     e1.insert('end',taipowerloc)
# #     text1.delete(1.0,'end')
# #     text1.insert('end','G:' + taipowerloc_dic['G']+'\n' + 'PP:' + str(taipowerloc_dic['PP'])+'\n' + 'QQ:' + str(taipowerloc_dic['QQ'])+'\n'
# #                  + 'R:'+ taipowerloc_dic['R'] + '\n' + 'S:' + taipowerloc_dic['S'] + '\n' + 'T:' + str(taipowerloc_dic['T']) +'\n' + 'U:' + 
# #                  str(taipowerloc_dic['U']) +'\n' + 'V:' + str(taipowerloc_dic['V']) +'\n' + 'W:' + str(taipowerloc_dic['W']))
  




def polequery(mypole):
    '請輸入台電桿號 : 西平高幹#1'
    import requests
    import json
    import urllib.parse
    
    mypole = urllib.parse.quote(mypole)

    url = "http://10.210.35.218/DMQService/api/PoleInformation/GetPoleInformation?TPCLID=&P_NUMB=" + mypole + "&COUNTY=&DISTRICT=&LI=&CODETXT="


    headers = {
        "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"ASP.NET_SessionId=0txljjjpxnuvxsauqnjsbejj"
    }

    r = requests.get(url,headers=headers)
    r = json.loads(r.text)
    mydict={}
    if "data" in r and len(r["data"]) > 0:
        # print(r["data"][0]["tpclid"])
        tpclid = r["data"][0]["tpclid"]
        for data in r["data"]:
            mydict[data["p_Numb"]] = data["tpclid"]
        
    else:
        # print("無此桿號")
        tpclid = "無此桿號"
    return tpclid,mydict


def tai_to_pole(tailoc:str)->str:

    '''請輸入台電桿號 : 西平高幹#1
       取得台電座標 G3320CB54'''
    import requests
    import json
    import urllib.parse
   
    My_Coordinate = tailoc #"G3416GA44" #urllib.parse.quote(tailoc)

    url = "http://10.210.35.218/DMQService/api/PoleInformation/GetPoleInformation?TPCLID=" + My_Coordinate + "&P_NUMB=&COUNTY=&DISTRICT=&LI=&CODETXT="


    headers = {
        "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"ASP.NET_SessionId=0txljjjpxnuvxsauqnjsbejj"
    }

    r = requests.get(url,headers=headers)
    r = json.loads(r.text)
    
    if "data" in r and len(r["data"]) > 0:
        # print(r["data"][0]["tpclid"])
        pole = r["data"][0]["p_Numb"]
    else:
        pole = "無此桿號"
    return pole


underground_dict={} 
def manhole_dict()->dict:
    """
    抓取所有人手孔資料及下載位置並回傳字典檔
    """
    import requests,json
    from bs4 import BeautifulSoup
    import datetime,os,time
    
    t1 = str(datetime.date.today()) #今天日期
    
    if os.path.isfile('manhole.txt'):
        timestamp = os.path.getmtime('manhole.txt')
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        t2 =  dt_object.strftime("%Y-%m-%d") #檔案修改時間
        if datetime.datetime.strptime(t2,"%Y-%m-%d") >= datetime.datetime.strptime(t1,"%Y-%m-%d"):
            print("檔案已為最新版")
            pass
        else:
            my_list =["G1100~G2799","G2800~G3452","G3500-G3938","G4000~G4036","G4100~G4234","G4300~G5202","K0577~K3999","K4073~K5899"]
            
            url = "http://10.210.35.206/graph/main.asp?folder=%A4H%A4%E2%A4%D5%A5d/" 

            for url in my_list:
                url = "http://10.210.35.206/graph/main.asp?folder=%A4H%A4%E2%A4%D5%A5d/" + url
                headers = {
                    "Connection":"keep-alive",
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":"ASPSESSIONIDCACRARAB=KBFLGNMDADOIDKMOHFCGEFBM",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }

                r = requests.get(url,headers=headers)
                r.encoding = "big5"

                soup = BeautifulSoup(r.text,"html.parser")
                # with open("underground.txt","w") as f:
                #     f.write(soup.prettify())

                
                for i in soup.find_all("a"):
                    key =(i.text).split(".")[0]
                    value = "ftp://10.210.35.206"  + i["href"].replace("album/","")
                    underground_dict[key] = value
            with open("manhole.txt" ,"w",encoding="utf8") as json_file:
                json.dump(underground_dict,json_file,ensure_ascii=False)
            return underground_dict
    else:
        
        my_list =["G1100~G2799","G2800~G3452","G3500~G3938","G4000~G4036","G4100~G4234","G4300~G5202","K0577~K3999","K4073~K5899"]
        
        url = "http://10.210.35.206/graph/main.asp?folder=%A4H%A4%E2%A4%D5%A5d/" 

        for url in my_list:
            url = "http://10.210.35.206/graph/main.asp?folder=%A4H%A4%E2%A4%D5%A5d/" + url
            headers = {
                "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "Cookie":"ASPSESSIONIDCACRARAB=KBFLGNMDADOIDKMOHFCGEFBM",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }

            r = requests.get(url,headers=headers)
            r.encoding = "big5"

            soup = BeautifulSoup(r.text,"html.parser")
            with open("underground.txt","w") as f:
                f.write(soup.prettify())

            
            for i in soup.find_all("a"):
                key =(i.text).split(".")[0]
                value = "ftp://10.210.35.206"  + i["href"].replace("album/","")
                underground_dict[key] = value
        with open("manhole.txt" ,"w",encoding="utf8") as json_file:
            json.dump(underground_dict,json_file,ensure_ascii=False)
        return underground_dict

def manhole_query(tailoc:str)->dict:
    """
    查詢人手孔資料 回饋tuple (座標,字典)
    字典 key:座標 ，value:地址
    """
    import json,requests
    My_manhol = tailoc #"G3416GA44" #urllib.parse.quote(tailoc)

    url = "http://10.210.35.218/DMQService/api/ManHandHoleQuery/GetManHandHoleQuery?TpclId=" + tailoc + "&Addr="


    headers = {
        "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"ASP.NET_SessionId=0txljjjpxnuvxsauqnjsbejj"
    }

    r = requests.get(url,headers=headers)
    r = json.loads(r.text)
    
    mydict={}
    if "data" in r and len(r["data"]) > 0:
        for data in r["data"]:
            mydict[data["tpclid"]] = data["addr"]
    else:
        mydict = "無此人手孔"
    return mydict


def dsbnroom_query(tailoc:str)->dict:
    """
    檢查有配場場室資料
    """
    import json,requests
    My_manhol = tailoc #"G3416GA44" #urllib.parse.quote(tailoc)

    url = "http://10.210.35.218/DMQService/api/DsbnroomInformation/GetDsbnroomInformation?" + tailoc + "=&BUILDING=&ADDR=&COUNTY=&DISTRICT=&LI=&CODETXT="


    headers = {
        "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"ASP.NET_SessionId=0txljjjpxnuvxsauqnjsbejj"
    }

    r = requests.get(url,headers=headers)
    r = json.loads(r.text)
        

    if "data" in r and len(r["data"]) > 0:
        # print(r["data"][0]["tpclid"])
        dsbnroom = r["data"][0]["tpclid"]
    else:
        dsbnroom = "無此配電室"
    return dsbnroom

def GetAddressOrNumber(address:str):
    import re
    given_string = address
    # 匹配地址
    address_pattern = r'\w+[縣市]?(\w+[市鎮])?([\w\d?鄉里村])?\w+[路段巷街][\u4e00-\u9fa5\d－、-]+?號(?<!地號)'
    myaddress = re.search(address_pattern, given_string)
    # print(f"=={given_string}=")

    if myaddress:
        
        # print("地址:", address.group().replace("/", ""))
        my_address = myaddress.group().replace("/", "")
    else:
        # print("無法找到地址")
        my_address = "無法找到地址"
    # 匹配地號
   
    number_pattern = r'彰化[縣市](\w+[市鎮])?(\w+[鄉里村])?(\w+段)?[\u4e00-\u9fa5\d－、-]+地號'
    number = re.search(number_pattern, given_string)
    if number:
        # print("地號:", number.group())
        my_number = number.group()
    else:
        # print("無法找到地號")
        my_number = "無法找到地號"
    return my_address,my_number


def AddressToCoordinate(address:str)->tuple:
    """
    將地址轉換為google座標
    
    """
    url =f"https://www.google.com.tw/search?tbm=map&authuser=0&hl=zh-TW&gl=tw&q={address}"
    import requests

    res = requests.get(url)

    #經度 lon 緯度 lat
    try:
        lon = res.text.split('@')[1].split(",")[1] #120.232
        lat = res.text.split('@')[1].split(",")[0] #24.123
        return lat,lon
    except:
        lat = "2" + res.text.split(',120')[0].split("null,2")[1][0:8]
        lon = "120" + res.text.split(',120')[1].split(",")[0][0:7]
        return lat,lon
def LandnoToLoc(town,section,landNo):
    """
    輸入地號取得座標
    town : 鄉鎮
    secton : 地段
    landNo : 地號
    回傳lat:24.12345 ,lon:120.12345  
    
    """
    
    import json
    import requests
    
    town_dict = {'二水鄉': '20', '二林鎮': '08', '大村鄉': '15', '大城鄉': '24', '北斗鎮': '04', '永靖鄉': '18', '田中鎮': '07',
                '田尾鄉': '21', '竹塘鄉': '25', '伸港鄉': '10', '秀水鄉': '12', '和美鎮': '03', '社頭鄉': '19', '芳苑鄉': '23',
                '花壇鄉': '13', '芬園鄉': '14', '員林市': '05', '埔心鄉': '17', '埔鹽鄉': '16', '埤頭鄉': '22', '鹿港鎮': '02',
                '溪州鄉': '26', '溪湖鎮': '06', '彰化市': '01', '福興鄉': '11', '線西鄉': '09'}  
    
    """
    從#取得各鄉鎮段號 https://easymap.land.moi.gov.tw/W10Web/City_json_getSectionList
        
    """
    url = "https://easymap.land.moi.gov.tw/W10Web/City_json_getSectionList"
    
    my_key = town_dict[town]
    
    payload = {
            'cityCode': 'N', # N 為彰化縣
            'townCode':f'{my_key}'
        }
    r = requests.post(url,data=payload)
    r = json.loads(r.text)
    
    
    #篩選該鄉鎮內地段到下拉選單
    # search_text = self.combo_box_2.currentText() #選取鄉鎮  
   
    section_id = ""
    officeCode = ""
                        
    #篩選符合條件的項目並加入下拉選單
    for section_data in r:
        if section_data['name'] == section:
            # print(f"id:{section_data['id']}" )
            section_id = section_data['id']
            officeCode = section_data['officeCode']
            
    #輸入地號取得座標
    """
    取得sectNo 地段名稱 office 及地號取得座標
    url = "https://easymap.land.moi.gov.tw/W10Web/Land_json_locate"
    payload = {'sectNo': '0602',
    'office': 'ND',
    'landNo': '1'}
    """ 
  
        # my_data = self.get_Section_data()
    url = "https://easymap.land.moi.gov.tw/W10Web/Land_json_locate"
    secNo = section_id
    office = officeCode
    
    landNo = landNo
    payload = {'sectNo': f'{secNo}',
    'office': f'{office}',
    'landNo': f'{landNo}'}
    #最終目標要有payload = {'sectNo': '0602','office': 'ND','landNo': '1'} 地段號碼 office 地號
    r = requests.post(url,data=payload)
    r = json.loads(r.text)

    lat = str(r["Y"])
    lon = str(r["X"])
    return lat,lon    

def landno_group(address):
    import re
    given_string = address
    # 匹配地址
    address_pattern = r'彰化[縣市](\w+[市鎮鄉里村])?(\w+段)?([\d－、-]+)地號'
    match = re.search(address_pattern, given_string)
    town = match.group(1)
    section = match.group(2)

    landno = match.group(3)
   
    if "、" in landno:
        landno = landno.split("、")[0]

    #將全寫改半寫
    def full_to_half(landno):
        # 使用正则表达式将全角数字和符号转换为半角
        landno = re.sub(r'０', '0', landno)
        landno = re.sub(r'１', '1', landno)
        landno = re.sub(r'２', '2', landno)
        landno = re.sub(r'３', '3', landno)
        landno = re.sub(r'４', '4', landno)
        landno = re.sub(r'５', '5', landno)
        landno = re.sub(r'６', '6', landno)
        landno = re.sub(r'７', '7', landno)
        landno = re.sub(r'８', '8', landno)
        landno = re.sub(r'９', '9', landno)
        landno = re.sub(r'－', '-', landno)  # 将全角减号转换为半角减号
        return landno
    landno = full_to_half(landno)
    return town,section,landno

       

if __name__ == "__main__":
    # # x = polequery("西平高幹#1")
    # print(tai_to_wgs("G3320CB52"))
    # print(type(taipower_loc(120.506112, 23.970121)))
    
   print(landno_group("彰化縣秀水鄉義雅巷臨１２９號/彰化縣秀水鄉馬興段４５０地號"))
    

