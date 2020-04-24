import os
import setting
import function
import datetime


#####  8時のpush通知  #####


now = datetime.datetime.now()
minute = [i for i in range(10)]


if now.hour == 23 and now.minute in minute:

    spredsheet_key_not_got_up = '10YxvUHRG9drcnAoyBxkls4vDN1mI9TSZq6XnJGy8aUk'
    worksheet_not_got_up = function.worksheet(spredsheet_key_not_got_up)

    #列の値を全て一次元配列に格納する（起きてない人のlist）
    not_got_up_list = worksheet_not_got_up.col_values(1)

    if not not_got_up_list:
        function.lineMessagingAPI("みんなよく起きれました！えらいにゃん！今日も一日頑張ってにゃんにゃん😸")

    else:
        message = function.message(not_got_up_list)
        function.lineMessagingAPI(message)


