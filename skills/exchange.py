from linebot.models import FlexSendMessage
from models.message_request import MessageRequest
from skills import add_skill
import pandas as pd
import json
import os

@add_skill('/匯率')
def get(message_request: MessageRequest):
    # /匯率 美金 1000
    msg_array = message_request.message.split()
    
    convert_currency = msg_array[1]
    twd = msg_array[2]
    
    result = convert(convert_currency, float(twd))
    
    flex = json.load(
        open(os.getcwd() + '\\skills\\' 'exchange.json', 'r', encoding='utf-8'))
    
    flex['body']['contents'][0]['text'] = f'匯率轉換 (新台幣 -> {convert_currency})'
    flex['body']['contents'][1]['text'] = f'新臺幣 {twd}'
    flex['body']['contents'][3]['text'] = f'可換得{convert_currency} {result}'
    
    msg = FlexSendMessage(alt_text='匯率轉換', contents=flex)
    
    return [
        msg
    ]


def convert(code: str, twd: float):
    # 用爬蟲取得表格內容
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    res = pd.read_html(url)
    df = res[0]
    
    # 取得全部 rows, 並前5筆column
    currency = df.iloc[:, :5]
    
    currency.columns = ["幣別", "現金匯率-本行買入",
                        "現金匯率-本行賣出", "即期匯率-本行買入", "即期匯率-本行賣出"]
    
    currency['幣別'] = currency['幣別'].str.extract('(\w+)')
      #美金 (USD)  美金 (USD) 修改為 美金 較好後續處理
    """extract() 方法:
這是 pandas 中 Series 對象的一個方法，用於從字串中提取匹配正則表達式的部分。
正則表達式 '(\w+)':

\w: 匹配任何字母、數字或下劃線字符。
+: 表示前面的模式（在這裡是 \w）應該出現一次或多次。
(): 括號用於創建一個捕獲組，extract() 方法會返回這個組匹配的內容。
使用extract 一定要使用()組別的方法，並只會傳回第一個"""
    # 進行轉換 filter(function, iterable)
    r = list(filter(lambda c: c[0] == code, currency.to_numpy()))
    val = float(r[0][2])
    
    result = round(twd/val, 5)
    
    return result