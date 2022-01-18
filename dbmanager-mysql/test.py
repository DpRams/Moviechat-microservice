import requests
import json


user_id = "Ub7385e82f5a34b097e8a12ec38601723"
my_params_get = {"user_id": user_id}
my_params_insert = {}

host = "http://192.168.1.170:5002"
get_booking = host + '/get/booking'
insert_booking = host + '/insert/booking'
delete_booking = host + '/delete/booking/all'

# get booking 
resp = requests.post(get_booking, data=json.dumps(my_params_get)) 

if resp.status_code == 200:
    data = json.loads(resp.text)
    print(data) #dict
else:
    print(f'HTTP Error code = {resp.status_code}')

# insert booking
# my_params_insert['id'] = 6
# my_params_insert['user_id'] = user_id
# my_params_insert['user_name'] = "李忠"
# my_params_insert['phone'] = "0934543566"
# my_params_insert['movie_name'] = "蜘蛛人"

# resp = requests.post(insert_booking, data=json.dumps(my_params_insert)) 

# delete booking all
# resp = requests.post(delete_booking) 

