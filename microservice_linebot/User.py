import requests
import json
from linebot.models import TextSendMessage

ticket_service_host = "https://microservice-ticket.herokuapp.com"
book_ticket_url = ticket_service_host + '/ticket'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class User:
    def __init__(self, uid, movie_obj):
        self.user_id = uid
        self.ordering = False
        self.order_id = None
        self.movie_name = None
        self.movie_obj = movie_obj

    def is_ordering(self):
        return self.ordering

    def cancel_ordering(self):
        self.ordering = False

    def click_booking(self, order_id):
        self.order_id = order_id
        movie_info = self.movie_obj.get_movie(rank=order_id)
        self.movie_name = movie_info['片名']
        self.ordering = True

    def order_ticket(self, event, user_name, phone, line_bot_api):
        data = {
            "user_id": self.user_id,
            "user_name": user_name,
            "phone": phone,
            "movie_name": self.movie_name,
        }
        print(data)

        resp = requests.post(
            book_ticket_url, json=data, headers=headers)

        if resp.status_code == 200:
            print('resp.text', resp.text)

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="訂票成功"))
        else:
            print(f'HTTP Error code = {resp.status_code}')
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="訂票失敗，請洽客服"))

        self.ordering = False

    def query_booking_history(self):
        data = {
            "user_id": self.user_id,
        }

        resp = requests.get(
            book_ticket_url, data=json.dumps(data), headers=headers)
        if resp.status_code == 200:
            pass
        else:
            print(f'HTTP Error code = {resp.status_code}')
            return False, resp.status_code

        return True, resp.text
