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

line_bot_api = LineBotApi('bi6ac8O1OyajuDnuAaQnd1A5B7PHludLuBTd+JKp5f8xX14sivkk7xPcI80VykvfqyE0z8ZrM/5pszNe8SwZouccjDEsHgTDe9XIQLPKxGE2aVAD2jlPHEnSGFczJ0d7WRxgwysuC7q2gYzwOBznhwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dff27d4fa24e26fae908e9f1f5aafeaf')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '不清楚您在說什麼耶..'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id = '6359',
            sticker_id = '11069850',
            )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', '嗨', 'Hi', '你好', 'Hello', '哈囉']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '當然囉'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位, 是嗎？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()