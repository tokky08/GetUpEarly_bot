from flask import Flask, request, abort
import os
import datetime
import schedule
import time
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_USER_ID = os.environ["YOUR_USER_ID"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def lineMessagingAPI(message):
    url = "https://script.google.com/macros/s/AKfycbyCzbcd4kTZk7PxLh-JkTJQTlXuUkY40FhWE5TXFOXQzYMTO3_f/exec?message="
    url = url + message
    result = requests.get(url)

schedule.every(1).minutes.do(lineMessagingAPI("テストだよ！"))

while True:
    schedule.run_pending()
    time.sleep(1)



# @app.route("/")
# def hello_world():
#     return "hello world!"

# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


# if __name__ == "__main__":
# #    app.run()
#     port = int(os.getenv("PORT"))
#     app.run(host="0.0.0.0", port=port)