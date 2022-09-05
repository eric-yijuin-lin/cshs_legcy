from datetime import datetime
import json
from flask import Flask, request, render_template
from linebot import LineBotApi, WebhookHandler
from modules.googlesheet import GoogleSheetHelper
from modules.student import StudentInfo
from modules.seat import SeatHelper, SeatInfo
from modules.schoolclass import ClassHelper, ClassInfo
from modules.registeration import RegisterationRow

with open('appConfig.json', 'r', encoding='utf-8') as fs:
    config = json.load(fs) # channelSecret & accessToken

app = Flask(__name__)
environment = config['environment']

sheet_helper = GoogleSheetHelper(
    config['googleSheet']["credential"],
    config['googleSheet']["url"]
)
line_bot_api = LineBotApi(config['lineBot']['accessToken'])
handler = WebhookHandler(config['lineBot']['channelSecret'])
seat_helper = SeatHelper()
class_helper = ClassHelper()

shadow_df = sheet_helper.read_all_as_df()

@app.route('/')
@app.route('/hello')
def hello():
    return 'hello world'

@app.route("/seat") # FUCK!! the data must be "string" here
def get_seat_form():
    seat_hash = request.args["seat_hash"]
    return render_template("seat_form.html", seat_hash=seat_hash)

@app.route("/seat", methods=["POST"])
def register_seat():
    try:
        student_info = StudentInfo(request.form)
        seat_info = seat_helper.get_seat_info(request.form)
        if environment == 'Production':
            class_info = class_helper.get_class_by_datetime()
        else:
            debug_date = datetime(2022, 9, 5, 8)
            class_info = class_helper.get_class_by_datetime(debug_date)

        validate_seat(seat_info, class_info)
        validate_class(student_info, class_info)
    except ValueError as ex:
        return str(ex), 400

    row = RegisterationRow(student_info, class_info, seat_info)
    if is_duplicate_registeration(row):
        return "重複簽到，請檢查「班級」、「座號」與座位卡", 400 
    try:
        doRegister(row)
        update_shadow(row)
    except Exception as ex:
        return str(ex), 500
    return "OK"

def validate_seat(seat_info: SeatInfo, class_info: ClassInfo):
    if seat_info.classroom != class_info.room:
        raise ValueError("教室與時間匹配錯誤，請檢查輸入")

def validate_class(student_info: StudentInfo, class_info: ClassInfo):
    if student_info.class_unit != class_info.unit:
        raise ValueError("班級與教室匹配錯誤，請檢查輸入")

def is_duplicate_registeration(row: RegisterationRow) -> bool:
    condition = (
        (shadow_df["班級"] == row.class_unit)
        & (shadow_df["座號"] == row.student_no)
    )
    if shadow_df[condition].any():
        return True
    condition = ((shadow_df["座位編號"] == row.room_seat_code))
    if shadow_df[condition].any():
        return True
    return False

def doRegister(registeration_row: RegisterationRow) -> None:
    sheet_helper.insert_row(registeration_row.to_list())

def update_shadow(registeration_row: RegisterationRow) -> None:
    shadow_df.append(registeration_row.to_list())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
