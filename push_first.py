from flask import Flask, request, abort
import os
import datetime
import schedule
import time
import requests


def lineMessagingAPI(message):
    url = "https://script.google.com/macros/s/AKfycbyCzbcd4kTZk7PxLh-JkTJQTlXuUkY40FhWE5TXFOXQzYMTO3_f/exec?message="
    url = url + message
    result = requests.get(url)

now = datetime.datetime.now()

if now.hour == 7:
    lineMessagingAPI("7時だよ！起きろ！8時までに返信がなければみんなに通知しますね！")




