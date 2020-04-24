import os
import gspread
import requests
from linebot import LineBotApi, WebhookHandler
from oauth2client.service_account import ServiceAccountCredentials 

def worksheet(spredsheet_key):

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    #辞書オブジェクト。認証に必要な情報をHerokuの環境変数から呼び出している
    credential = {
        "type": "service_account",
        "project_id": os.environ['SHEET_PROJECT_ID'],
        "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
        "private_key": os.environ['SHEET_PRIVATE_KEY'],
        "client_email": os.environ['SHEET_CLIENT_EMAIL'],
        "client_id": os.environ['SHEET_CLIENT_ID'],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ['SHEET_CLIENT_X509_CERT_URL']
    }
    

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = spredsheet_key

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    return worksheet



def lineMessagingAPI(message):
    url = "https://script.google.com/macros/s/AKfycbyCzbcd4kTZk7PxLh-JkTJQTlXuUkY40FhWE5TXFOXQzYMTO3_f/exec?message="
    url = url + message
    result = requests.get(url)


def message(not_got_up_list):
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
        
    message = message + "さんは起きてません！起こしてあげてにゃん！😾"

    return message