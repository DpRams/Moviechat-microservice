import pymysql
import pandas as pd
import os
from flask import Flask, jsonify
import flask
import configparser
import requests
import json
import logging

#https://stackoverflow.com/questions/30085538/change-flask-logs-from-info-to-debug
logger = logging.getLogger("mypackage.mymodule")  # or __name__ for current module
logger.setLevel(logging.ERROR)

app = Flask(__name__)

try:
    username = os.environ['username']
    passwd = os.environ['passwd']
    host = os.environ['host']
    db = os.environ['db']
except:
    config = configparser.ConfigParser()
    config.read('./mysql.ini')
    username = config.get('mysql-url', 'username')
    passwd = config.get('mysql-url', 'passwd')
    host = config.get('mysql-url', 'host')
    db = config.get('mysql-url', 'db')

conn = pymysql.connect(host=host, port=3306, user=username, passwd=passwd, db=db, charset='utf8')

@app.route("/", methods=['GET'])
def connect():
    
    return "已建立連線" #conn


@app.route("/get/booking", methods=['POST']) #傳入user_id，用POST?
def get_booking():
    
    params = json.loads(flask.request.get_data(as_text=True))
    cursor = conn.cursor()
    cursor.execute(f"select * from booking where user_id = '{params['user_id']}'") #['user_id']
    data = cursor.fetchall()  
    # print(data)
    booking_data = {}
    booking_datas = {'data':[]}
    column_names = []
    column_infos = cursor.description

    for col in column_infos:
        column_names.append(col[0])

    for i in range(len(data)):
        for j in range(len(column_names)):
            booking_data[column_names[j]] = data[i][j]
        booking_datas['data'].append(booking_data)
        booking_data = {}
    # print(booking_datas)
    return booking_datas

@app.route("/insert/booking", methods=['POST']) #傳入user_id，用POST?
def insert_booking():
    params = json.loads(flask.request.get_data(as_text=True))
    cursor = conn.cursor()
    cursor.execute(f"insert into booking (user_id, user_name, phone, movie_name) values ('{params['user_id']}','{params['user_name']}','{params['phone']}','{params['movie_name']}')")
    conn.commit()
    return "已新增一筆資料"


@app.route("/delete/booking/all", methods=['POST']) #傳入user_id，用POST?
def delete_booking_all():
    __clear_all_datas()
    return "已刪除所有資料"

def __clear_all_datas():

    sql_del_data = """
    DELETE FROM booking
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql_del_data)
        conn.commit()
    except Exception as e:
        print(e)


# def initialize(conn):

#     __clear_all_datas(conn)
#     __create_tables(conn)

#     return "Initialize the database(clear all data) : done"

# def rebuild(conn):

#     __drop_all_tables(conn)
#     __create_tables(conn)

#     return "Rebuild the database : done"

# def get_tables(conn):

#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("SHOW TABLES")
#         tables = cursor.fetchall()  
#     except Exception as e:
#         print(e)

#     return tables

# def __drop_all_tables(conn): #重新規劃資料表使用

#     sql_drop_table= """
#     DROP TABLE IF EXISTS booking
#     DROP TABLE IF EXISTS movies_rank
#     """
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql_drop_table)
#         conn.commit()
#     except Exception as e:
#         print(e)

# def __create_tables(conn):
    
#     sql_c_booking = """
#     CREATE TABLE booking (
#     id int(10) NOT NULL,
#     user_id varchar(50) NOT NULL,
#     user_name varchar(50) NOT NULL,
#     phone varchar(50) NOT NULL,
#     movie_name varchar(50) NOT NULL,
#     PRIMARY KEY (id)
#     ) 
#     """
#     # sql_c_movies_rank = """
#     # CREATE TABLE movies_rank (
#     # id int(10) NOT NULL,
#     # rank int(10) NOT NULL,
#     # movies_name varchar(50) NOT NULL,
#     # rate double NOT NULL,
#     # web_link varchar(1000) NOT NULL,
#     # poster_link varchar(1000) NOT NULL,
#     # date date NOT NULL,
#     # length varchar(50) NOT NULL,
#     # company varchar(50) NOT NULL,
#     # director varchar(50) NOT NULL,
#     # introduction varchar(1000) NOT NULL,
#     # timetable_link varchar(1000) NOT NULL,
#     # screenshot_link varchar(1000) NOT NULL,
#     # screenshot_file_link varchar(1000) NOT NULL,
#     # PRIMARY KEY (id)
#     # ) 
#     # """

#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql_c_booking)
#         # cursor.execute(sql_c_movies_rank)
#         conn.commit()
#     except Exception as e:
#         print(e)

# def __read_data():
#     # df = pd.read_excel('./movies_info.xlsx')
#     pass
#     # return df


if __name__ == "__main__":    
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host='0.0.0.0', port=port)   



#https://zhangshehua.com/1634201309.html