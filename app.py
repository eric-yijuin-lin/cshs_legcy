from calendar import weekday
from datetime import datetime
import json
from modules.seat import SeatHelper, SeatInfo
from modules.schoolclass import ClassHelper, ClassInfo
from crypt import methods
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage

from modules.student import StudentInfo


with open('api_credential.json', 'r', encoding='utf-8') as fs:
    config = json.load(fs) # channelSecret & accessToken

app = Flask(__name__)
line_bot_api = LineBotApi(config['accessToken'])
handler = WebhookHandler(config['channelSecret'])
seat_helper = SeatHelper()
class_helper = ClassHelper()

@app.route('/')
@app.route('/hello')
def hello():
    return 'hello world'

@app.route("/seat/<int:seat_hash>")
def get_seat_form(seat_id: str):
    return render_template("seat_form.html", seat_id=seat_id)

@app.route("/seat", methods=["POST"])
def register_seat():
    student_info = StudentInfo(request.form)
    seat_info = seat_helper.get_seat_info(request.form)
    class_info = class_helper.get_class_by_datetime()
    try:
        validate_seat(seat_info, class_info)
        validate_class(student_info, class_info)
    except ValueError as ex:
        return str(ex), 400


def validate_seat(seat_info: SeatInfo, class_info: ClassInfo):
    if seat_info.classroom != class_info.room:
        raise ValueError("教室與時間匹配錯誤，請檢查輸入")
def validate_class(student_info: StudentInfo, class_info: ClassInfo):
    if student_info.class_unit != class_info.unit:
        raise ValueError("班級與教室匹配錯誤，請檢查輸入")
# @app.route('/callback', methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)
#     try:
#         handler.handle(body, signature)
#     except Exception as ex:
#         print('發生未預期錯誤：', ex)
#         abort(400) # 回傳 Http 400 error (錯誤的請求)
#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))

# @handler.add(MessageEvent, message=StickerMessage)
# def handle_message2(event):
#     print(event.reply_token)
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Sticker~~'))
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
