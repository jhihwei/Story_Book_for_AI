# coding: utf-8

# 引用Web Server套件
from random import randrange

import codecs
from flask import Flask, request, abort, send_from_directory, make_response, send_file

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# 載入基礎設定檔
secretFileContentJson = json.load(open("./line_secret_key", 'r', encoding='utf8'))
server_url = secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__, static_url_path="", static_folder="")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))


# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
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

# 引用以後可能會用到的套件
from linebot.models import (
    ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage,
    AudioSendMessage, StickerSendMessage)

from linebot.models.template import *

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage
)
import requests, uuid
from coco import *
from timeit import default_timer as timer
# 文字消息處理
@handler.add(MessageEvent, message=ImageMessage)
def process_image_message(event):
    start = timer()
    print("聊天室收到圖片: ", start)
    token = secretFileContentJson.get("channel_access_token")
    header = {'Authorization': 'Bearer ' + token}
    url = f'https://api.line.me/v2/bot/message/{event.message.id}/content'
    image = requests.get(url, headers=header)
    print("下載圖片")
    image_name = f'images/{str(uuid.uuid4())}.png'
    open(image_name, 'wb').write(image.content)
    body = request.get_data(as_text=True)
    print(body)
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        print("翻譯圖片")
        reply_message = translate(image_name)
        reply_message = reply_message.replace("<start>", "")
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text=reply_message),
            ]
        )
    end = timer()
    print("執行時間: ", end - start)
    return 'OK'

from linebot.models import PostbackEvent
from urllib.parse import parse_qs

@handler.add(PostbackEvent)
def process_postback_event(event):
    query_string_dict = parse_qs(event.postback.data)
    line_bot_api.reply_message(
        event.reply_token,
        []
    )


'''

Application 運行（開發版）

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)

'''

Application 運行（heroku版）

'''

# import os
# if __name__ == "__main__":
#     app.run(host='0.0.0.0',port=os.environ['PORT'])
