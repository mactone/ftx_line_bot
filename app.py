import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# FTX
from ftx import FtxClient
from utilityFunctions
from ftxQuery import getSpotMarginProfit

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

# FTX
subaccount = FtxClient(os.environ.get("API_KEY"),
                       os.environ.get("API_SECRET"),
                       os.environ.get("SUBACCOUNT_NAME"))
coinlist = ['SOL-PERP','FTM-PERP','FTT-PERP'] #套利幣種


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    if(get_message=="查詢套利收益"):
        reply=getSpotMarginProfit(subaccount,coinlist)
    else:
        reply = TextSendMessage(text=f"{get_message}")
    # Send To Line
    line_bot_api.reply_message(event.reply_token, reply)
