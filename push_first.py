import setting
import function


##### 7時のpush通知 #####

#起きれた人のスプレッドシートを一度全消去する
spredsheet_key_got_up = '1uqKc2v-hgOD7QMNdqjgF3NhLc3e3mlY8V2C15brBoUQ'
worksheet_got_up = function.worksheet(spredsheet_key_got_up)
worksheet_got_up.clear()


#起きれてない人のスプレッドシートを一度全消去する
spredsheet_key_not_got_up = '10YxvUHRG9drcnAoyBxkls4vDN1mI9TSZq6XnJGy8aUk'
worksheet_not_got_up = function.worksheet(spredsheet_key_not_got_up)
worksheet_not_got_up.clear()


function.lineMessagingAPI("起きろにゃん！！！8時までに返信がなければみんなに通知するにゃん😼")

