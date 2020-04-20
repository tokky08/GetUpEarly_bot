from flask import Flask, request, abort
import os
import sys
import datetime
import schedule
import time
import requests
import gspread
import json
import setting
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 



def worksheet(spredsheet_key):

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # 辞書オブジェクト。認証に必要な情報をHerokuの環境変数から呼び出している
    credential = {
        "type": "SERVICE_ACCOUNT",
        "project_id": os.environ['SHEET_PROJECT_ID'],
        "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
        "private_key": os.environ['SHEET_PRIVATE_KEY'],
        "client_email": os.environ['SHEET_CLIENT_EMAIL'],
        "client_id": os.environ['SHEET_CLIENT_ID'],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
    }

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)
    # credentials = ServiceAccountCredentials.from_json_keyfile_name("getupearly-8091651365a4.json", scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = spredsheet_key

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    return worksheet


#起きれた人のスプレッドシートを一度全消去する
spredsheet_key_got_up = '1uqKc2v-hgOD7QMNdqjgF3NhLc3e3mlY8V2C15brBoUQ'
worksheet_got_up = worksheet(spredsheet_key_got_up)
worksheet_got_up.clear()


#起きれてない人のスプレッドシートを一度全消去する
spredsheet_key_not_got_up = '10YxvUHRG9drcnAoyBxkls4vDN1mI9TSZq6XnJGy8aUk'
worksheet_not_got_up = worksheet(spredsheet_key_not_got_up)
worksheet_not_got_up.clear()


def lineMessagingAPI(message):
    url = "https://script.google.com/macros/s/AKfycbyCzbcd4kTZk7PxLh-JkTJQTlXuUkY40FhWE5TXFOXQzYMTO3_f/exec?message="
    url = url + message
    result = requests.get(url)


#####  7時にpush通知する処理  ########

now = datetime.datetime.now()
if now.hour == 7:
    lineMessagingAPI("7時だよ！起きろ！8時までに返信がなければみんなに通知しますね！")
else:
    print("テスト")
    sys.exit()

# 1時間5分待つ
hour = 60*65
time.sleep(hour)

#####  8時に起きてない人達のための処理  #########

now = datetime.datetime.now()
if now.hour == 8:

    spredsheet_key_not_got_up = '10YxvUHRG9drcnAoyBxkls4vDN1mI9TSZq6XnJGy8aUk'
    worksheet_not_got_up = worksheet(spredsheet_key_not_got_up)

    #列の値を全て一次元配列に格納する（起きてない人のlist）
    not_got_up_list = worksheet.col_values(1)

    if not not_got_up_list:
        lineMessagingAPI("みんなよく起きれました！えらい！")
        sys.exit()

    else:

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
        lineMessagingAPI(message)

else:
    sys.exit()

