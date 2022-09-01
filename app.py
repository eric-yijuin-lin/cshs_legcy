import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage

with open('api_credential.json', 'r', encoding='utf-8') as fs:
    config = json.load(fs) # channelSecret & accessToken

app = Flask(__name__)
line_bot_api = LineBotApi(config['accessToken'])
handler = WebhookHandler(config['channelSecret'])

@app.route('/')
@app.route('/hello')
def hello():
    return 'hello world'

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as ex:
        print('發生未預期錯誤：', ex)
        abort(400) # 回傳 Http 400 error (錯誤的請求)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_message2(event):
    print(event.reply_token)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Sticker~~'))

if __name__ == '__main__':
    app.run()
