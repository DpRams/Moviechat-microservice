import pymysql
import pandas as pd
import os


def connect(username, passwd, host, db):
    conn = pymysql.connect(host=host, port=3306, user=username,
                           passwd=passwd, db=db, charset='utf8')
    return conn


def initialize(conn):

    __clear_all_datas(conn)
    __create_tables(conn)

    return "Initialize the database(clear all data) : done"


def rebuild(conn):

    __drop_all_tables(conn)
    __create_tables(conn)

    return "Rebuild the database : done"


def get_tables(conn):

    cursor = conn.cursor()

    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
    except Exception as e:
        print(e)

    return tables


def __clear_all_datas(conn):

    sql_del_data = """
    DELETE FROM booking
    DELETE FROM movies_rank
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql_del_data)
        conn.commit()
    except Exception as e:
        print(e)


def __drop_all_tables(conn):  # 重新規劃資料表使用

    sql_drop_table = """
    DROP TABLE IF EXISTS booking
    DROP TABLE IF EXISTS movies_rank
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql_drop_table)
        conn.commit()
    except Exception as e:
        print(e)


def __create_tables(conn):

    sql_c_booking = """
    CREATE TABLE booking (
    id int(10) NOT NULL AUTO_INCREMENT,
    user_id varchar(50) NOT NULL,
    user_name varchar(50) NOT NULL,
    phone varchar(50) NOT NULL,
    movie_name varchar(50) NOT NULL,
    PRIMARY KEY (id)
    ) 
    """
    sql_c_movies_rank = """
    CREATE TABLE movies_rank (
    id int(10) NOT NULL AUTO_INCREMENT,
    rank int(10) NOT NULL,
    movies_name varchar(50) NOT NULL,
    rate double NOT NULL,
    web_link varchar(1000) NOT NULL,
    poster_link varchar(1000) NOT NULL,
    date date NOT NULL,
    length varchar(50) NOT NULL,
    company varchar(50) NOT NULL,
    director varchar(50) NOT NULL,
    introduction varchar(1000) NOT NULL,
    timetable_link varchar(1000) NOT NULL,
    screenshot_link varchar(1000) NOT NULL,
    screenshot_file_link varchar(1000) NOT NULL,
    PRIMARY KEY (id)
    ) 
    """

    cursor = conn.cursor()
    try:
        cursor.execute(sql_c_booking)
        cursor.execute(sql_c_movies_rank)
        conn.commit()
    except Exception as e:
        print(e)


def __read_data():
    df = pd.read_excel('./movies_info.xlsx')

    return df


def insert_movie(conn):
    df = __read_data()
    sql_insert = f"""
    INSERT INTO movies_rank
    (id, rank, movies_name, rate, web_link, poster_link, date, length, company, director, introduction, timetable_link, screenshot_link, screenshot_file_link)
    VALUES
    ({df.iloc[0][0]}, {df.iloc[0][1]},)
    
    """
# df = pd.read_excel('./movies_info.xlsx')
# print(df.iloc[0][])
