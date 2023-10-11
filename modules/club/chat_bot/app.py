import json
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent
)
import os
print("Current Working Directory:", os.getcwd())
from bot_commands.command_base import CommandBase
from secret_number_game.game_manager import SecretNumberGameManager


app = Flask(__name__)
credential: dict = None
command_config: dict = None
secret_number_manager = SecretNumberGameManager()

try:
    with open('./api_credential.json', 'r', encoding='utf-8') as fs:
        credential = json.load(fs) # channelSecret & accessToken
        configuration = Configuration(access_token = credential['accessToken'])
        handler = WebhookHandler(credential['channelSecret'])
except FileNotFoundError:
    print('failed to load credential')
    quit("the LINE bot API is terminated")

# try:
#     with open('./command_config.json', 'r', encoding='utf-8') as fs:
#         config = json.load(fs)
#         CommandBase.set_static_config(config)
# except FileNotFoundError:
#     print('failed to load command configuration')
#     quit("the LINE bot API is terminated")


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        group_id = event.source.group_id
        user_id = event.source.user_id
        name = ""
        reply_msg = ""
        profile = None

        if event.source.group_id:
            profile = line_bot_api.get_group_member_profile(group_id, user_id)
        else:
            profile = line_bot_api.get_profile(user_id)
        name = profile.display_name

        if event.message.text == "debug":
            reply_msg = f"display_name: {name}, \nevent: {event}"
        elif event.message.text[0] == '/':
            arguments = event.message.text.split(' ')
            if arguments[0] == "/number":
                result = secret_number_manager.process_command(user_id, name, arguments)
                if result.message:
                    reply_msg = result.message
            else:
                reply_msg = f"目前版本不支援 {arguments[0]} 指令"
                
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_msg)]
            )
        )

@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="Sticker~~~")]
            )
        )

if __name__ == "__main__":
    app.run()