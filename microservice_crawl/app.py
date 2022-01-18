#https://www.delftstack.com/zh-tw/howto/python-pandas/convert-pandas-dataframe-to-dictionary/
import requests
import pandas as pd
from flask import Flask
import os
import crawl
import logging
import json

#https://stackoverflow.com/questions/30085538/change-flask-logs-from-info-to-debug
logger = logging.getLogger("mypackage.mymodule")  # or __name__ for current module
logger.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

@app.route("/", methods=['GET'])
def index():
    return "Hello World!"

@app.route("/crawl", methods=['GET'])
def index_crawl():
    movies_df = crawl.crawling('https://movies.yahoo.com.tw/chart.html')
    print("Crawling完畢")
    movies_df = movies_df
    movies_json = movies_df.to_json(orient='table', force_ascii=False, index=False) #此index是指0,1,2，不是column definition
    temp = eval(movies_json)['data'] #movies_json有schema, data，只要data
    movies_json = {} #初始化movies_json
    movies_json['data'] = temp #賦予'data':temp
    return json.dumps(movies_json, ensure_ascii=False).encode('utf8')

# @app.route("/sqlfile/init", methods=['GET'])
# def sqlfile_init():
#     msg = sqlfile.initialize(conn)
#     return msg

# @app.route("/sqlfile/view", methods=['GET'])
# def sqlfile_view():
#     tables = sqlfile.get_tables(conn)
#     return tables

# @app.route("/sqlfile/rebuild", methods=['GET'])
# def sqlfile_rebuild():
#     msg = sqlfile.rebuild(conn)
#     return msg

if __name__ == "__main__":    
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)    
