from flask import Flask, request, abort

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

line_bot_api = LineBotApi('+YNhcud2UVU0HXtBAWFXt28kkL82etfxDPxG/RJuUqjUpzwVfl33eIjwqBjwgXBFY9MyA0PAvQGFL9L6PnRxAtj8wT/lERdp9CBq6syl7oOFRjNUdqb1SJ3ASmTKIONJJyWCUg4+kG/BLOKwHgv0HgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0be1b93468d619d5ab0ae2f45f7fe50')


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
    s = '你吃飯了嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()