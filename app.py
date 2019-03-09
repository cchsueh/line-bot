from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('X76OjCTr8U1wdP5xvRLeTS08T8quq8TshjU/ymrypVr8GAg9Gf/JV++Bn2b6PZTfY9MyA0PAvQGFL9L6PnRxAtj8wT/lERdp9CBq6syl7oNZ1iUOQLuJ8VannudrEdk/AOTBAsla9qCdHQf+Cs+5/wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5ed13c3b1bfa489bc868d0d2203d1725')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '給我貼圖':
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sticker_message))

    r = '很抱歉，您說什麼'
    if msg == ['hi', 'HI']:
        r = '嗨'
    elif msg == '你是誰':
        r = '我是機器人'
    elif msg == '你吃飯了嗎':
        r = '還沒'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()