from __future__ import unicode_literals
import os
from flask import Flask, request, abort  # , session
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import configparser
import json

import json_process
import re
import pandas as pd
import sys
import requests
import time
from User import User
from Movie import Movie

import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


# ticket_service_host = "https://microservice-ticket.herokuapp.com"
ticket_service_host = "http://10.108.42.106:5003"
book_ticket_url = ticket_service_host + '/ticket'

# crawl_service_host = 'https://mcs-crawl.herokuapp.com'
crawl_service_host = 'http://10.109.2.55:5001'
crawl_ranking_url = crawl_service_host + '/crawl'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

user_dict = dict()

# LINE 聊天機器人的基本資料
try:
    # set in Heroku
    line_access_token = os.environ['line_access_token']
    line_secret = os.environ['line_secret']
except:
    print('read config.ini')
    config = configparser.ConfigParser()
    config.read('config.ini')
    line_access_token = config.get('line-bot', 'line_access_token')
    line_secret = config.get('line-bot', 'line_secret')


line_bot_api = LineBotApi(line_access_token)
handler = WebhookHandler(line_secret)

# movies_df = pd.read_excel('./movies_info.xlsx')
movie_obj = Movie()

last_crawl_time = 0


@app.route("/", methods=['GET'])
def index():
    return "Good!"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

# #此段可藉由user回覆LineBot後，便可取得user_id，有user_id，就能主動推撥(Push)訊息給user(尚未成熟)
# def get_id(event):
#     user_id = event.source.user_id
#     print("user_id =", user_id)

#     try:
#         line_bot_api.push_message(user_id, TextSendMessage(text="請輸入1~20的數字，查詢電影排行榜"))
#     except Exception as e:
#         print(e)


def get_user(event) -> User:
    global user_dict
    user_id = event.source.user_id
    user = None
    if (user_id not in user_dict):
        user = User(user_id, movie_obj)
        user_dict[user_id] = user
    else:
        user = user_dict[user_id]
    return user


@handler.add(MessageEvent, message=TextMessage)
def movies(event):
    value_rank = re.compile(r'^排行榜 *(2[0]|1[0-9]|[1-9])$')
    result_rank = value_rank.match(event.message.text)

    user = get_user(event)

    if result_rank:
        id = eval(event.message.text[3:])
        crawl_movie()
        id = movie_obj.check_len(id)
        movies_dict = movie_obj.get_movie(rank=id)

        json_process.rank(movies_dict, id)
        FlexMessage = json.load(open('rank.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            'Movie Introduction', FlexMessage))
        user.cancel_ordering()

    elif event.message.text == "查詢":
        ok, history = user.query_booking_history()

        if ok:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=history))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="伺服器維護中"))

    if user.is_ordering():
        user_name, phone = event.message.text.split(" ")
        user.order_ticket(event, user_name, phone, line_bot_api)
        print(user_name, phone)

    sys.stdout.flush()


@ handler.add(PostbackEvent)
def handle_postback(event):
    data = json.loads(event.postback.data)
    id = int(data['rank'])
    action = data['action']
    print('rank:', id, action)

    if action == '劇照':
        reply_movie_photos(event, data)
    elif action == '訂票':
        user = get_user(event)
        user.click_booking(id)

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入姓名及電話(空白分隔)"))
        print('訂票')

    sys.stdout.flush()


def reply_movie_photos(event, data):
    id = int(data['rank'])
    # TemplateMessage = json.load(open('poster.json','r',encoding='utf-8'))
    image_url = movie_obj.get_movie_photo_urls(id)

    if len(image_url) != 0:
        columns = [ImageCarouselColumn(
            image_url=image_url[i],
            action=MessageTemplateAction(
                label=movie_obj.get_movie_name(id),
                text="劇照"
            )
        ) for i in range(5)]
        carousel_template = ImageCarouselTemplate(columns=columns)

    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text="電影劇照", template=carousel_template))  # TemplateSendMessage('profile',TemplateMessage)


def crawl_movie():
    global last_crawl_time

    if time.time() - last_crawl_time >= 3600:
        print('超過一小時，重新爬取排行榜')
        res = requests.get(crawl_ranking_url)
        last_crawl_time = time.time()

        data = res.text
        data = data.replace('\\', '')
        data = data.replace('\r', '')
        data = data.replace('\n', '')
        data = json.loads(data)
        movies_df = pd.DataFrame(data['data'])
        movies_df['劇照'] = movies_df['劇照'].apply(str)
        movie_obj.update_movie(movies_df)
    else:
        print('use cache data')

    sys.stdout.flush()


# line_bot_api.push_message("Ub7385e82f5a34b097e8a12ec38601723", TextSendMessage(text="請輸入1~20的數字，查詢電影排行榜"))
# id = 1
# movies_dict = get_movie(movies_df, rank=id)
# json_process.rank(movies_dict, id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host='0.0.0.0', port=port)
