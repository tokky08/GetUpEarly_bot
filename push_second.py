from flask import Flask, request, abort
import os
import datetime
import schedule
import time
import requests

import gspread
import json
import setting

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('getupearly-8091651365a4.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '10YxvUHRG9drcnAoyBxkls4vDN1mI9TSZq6XnJGy8aUk'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#列の値を全て一次元配列に格納する（起きてない人のlist）
not_got_up_list = worksheet.col_values(1)



user_id_list = []
for user_id in not_got_up_list:
    user_id_list.append(user_id)
    

YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

profile_list = []
for user_id in user_id_list:
    profile = line_bot_api.get_profile(user_id)
    profile_list.append(profile)

name_list = []
for profile in profile_list:
    name = profile.display_name
    name_list.append(name)


message = ''
for name in name_list:
    message += name + ", "
    
message = message + "さんは起きてません！起こしてあげて〜！"



def lineMessagingAPI(message):
    url = "https://script.google.com/macros/s/AKfycbyCzbcd4kTZk7PxLh-JkTJQTlXuUkY40FhWE5TXFOXQzYMTO3_f/exec?message="
    url = url + message
    result = requests.get(url)

lineMessagingAPI(message)


