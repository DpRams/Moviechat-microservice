import os
from flask import Flask, request, abort  # , session

import json
import requests
import sys
import logging
import pandas as pd

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

dbmgr_service_host = "https://dbmanager-mysql.herokuapp.com"

insert_booking_url = dbmgr_service_host + '/insert/booking'
get_booking_url = dbmgr_service_host + '/get/booking'


@app.route("/", methods=['GET'])
def index():
    return "Ticket Service"


@app.route("/ticket", methods=['GET', 'POST'])
def ticket():
    result = 500
    data = request.get_data()
    if request.method == 'GET':
        # 查詢使用者訂票紀錄
        """
        data = {"user_id": uid}
        """
        res = requests.post(get_booking_url, data=data, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            df = pd.DataFrame(data['data'])
            history_booking_str = get_history_booking_str(df)
            print(history_booking_str)
            result = history_booking_str
        else:
            print(f'HTTP Error code = {res.status_code}')
            result = res.status_code

    elif request.method == 'POST':
        # 新增一筆新的訂票
        """
        data = {
            "user_id": uid,
            "user_name": user_name,
            "phone": phone,
            "movie_name": movie_name,
        }
        """
        data = request.get_data()
        success, res = book_ticket(data)
        if success:
            print(res.text)
            result = res.text
        else:
            print(f'HTTP Error code = {res.status_code}')
            result = res.status_code

    sys.stdout.flush()
    return str(result)


def book_ticket(booking_info):
    booking_info = json.loads(booking_info)
    print('book_ticket:', booking_info)
    booking_info = json.dumps(booking_info)
    resp = requests.post(insert_booking_url,
                         data=booking_info, headers=headers)

    if resp.status_code == 200:
        return True, resp
    else:
        print(f'HTTP Error code = {resp.status_code}')
        return False, resp


def get_history_booking_str(dataframe):
    result = ''
    for i in range(len(dataframe)):
        row = dataframe.iloc[i]
        result += f"""
電影名稱: {row['movie_name']}
姓名: {row['user_name']}
電話: {row['phone']}
"""
    return result


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
