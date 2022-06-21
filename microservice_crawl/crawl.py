#https://www.delftstack.com/zh-tw/howto/python-pandas/convert-pandas-dataframe-to-dictionary/
import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawling(url): #'https://movies.yahoo.com.tw/chart.html'
    response = requests.get(url=url)
  
    soup = BeautifulSoup(response.text, 'lxml')

    rows = soup.find_all('div', class_='tr')
    colname = list(rows.pop(0).stripped_strings) #把欄位名稱pop出來，使第一筆資料即為電影資訊
    hrefs = soup.select('div.td > a') #電影資訊連結(包括預告片等等)

    #擷取電影資訊連結
    links = []
    for href in hrefs:
        a = href.get('href')
        if not a.endswith('.html'): #電影資訊頁面 的連結結尾沒有.html
            links.append(a) 

    #將排名、片名、評分、連結置入data(list)
    data = []
    for i in range(len(rows)):

      data.append([i+1])
      data_in = False
      find_a = rows[i].find('a')
      #判斷電影是否有資訊連結
      if find_a:
          find_href = find_a.get('href')
          if find_href:
              data_in = True
          else:
              data[i].append(None)
              continue
      else:
          data[i].append(None)
          continue

      #若有資訊連結(才可繼續後面的相關資料蒐集)
      if data_in == True:
      
          try:
              a = eval(list(rows[i].stripped_strings)[1]) # 因為[1]筆資料可能是上周排序或是片名，所以此處如果eval成功(代表是排序)則擷取[2](片名)
              data[i].append(list(rows[i].stripped_strings)[2])
          except:
              data[i].append(list(rows[i].stripped_strings)[1]) # 若因eval報錯，則[1]就是片名。
          data[i].append(list(rows[i].stripped_strings)[-1]) # [-1]為電影評分
          data[i].append(find_href) # 電影資訊連結


    #將data置入dataframe
    data_df = pd.DataFrame(data, columns = ["本周排名","片名","評分","連結"])
    data_df.dropna(inplace=True) #去除資料不完整的電影資訊
    data_df['本周排名'] = [i+1 for i in range(data_df.shape[0])] #重新排名
    data_df.reset_index(drop=True,inplace=True)
    #data_df

    #擷取上映日期、片長、發行公司
    date = []  
    time = []
    firm = []
    director = []
    intro = []
    img = []
    time_url = []
    poster = []

    for url in data_df['連結']:
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.select("div.movie_intro_info_r > span")
        
        #擷取上映日期、片長、發行公司
        for i in range(3): #0~2 ["上映日期", "片長","發行公司"]
            index_colon = infos[i].string.find("：")
            if i == 0: #上映日期
                date.append(str(infos[i].string)[index_colon+1:])
            elif i == 1: #片長 
                time.append(str(infos[i].string)[index_colon+1:])
            elif i == 2: #發行公司
                firm.append(str(infos[i].string)[index_colon+1:]) 


        directors = soup.select("span.movie_intro_list")
        # print(directors[0].text.replace("導演：","").strip())
        # if (directors[0].string) == None:
        #   directors = soup.select("div.movie_intro_list > a")

        director.append(directors[0].text.replace("導演：","").strip())

        #擷取劇情介紹
        infos = soup.select("div.gray_infobox_inner > span")
        intro.append(str(infos[0].string).strip()) 

        #電影海報
        infos = soup.select("div.movie_intro_foto > img")
        img.append(infos[0]['src'])

        #時刻表連結
        movie_id = url[-5:] #電影id目前只使用到10000多，若電影編號小於10000或大於99999，則可以擷取"="後面的數字。
        time_url.append(f"https://movies.yahoo.com.tw/movietime_result.html?movie_id={movie_id}")

        #劇照連結
        poster.append(f'https://movies.yahoo.com.tw/movieinfo_photos.html/id={movie_id}')
      
    data_df["電影海報"] = img
    data_df["上映日期"] = date
    data_df["片長"] = time
    data_df["發行公司"] = firm
    data_df["導演"] = director
    data_df["劇情介紹"] = intro
    data_df['時刻表連結'] = time_url
    data_df['劇照連結'] = poster

    poster_url = []
    for i in range(len(data_df['劇照連結'])):
        poster_url.append([])
        response = requests.get(url=data_df['劇照連結'][i])

        soup = BeautifulSoup(response.text, 'lxml')
        poster_link = soup.find_all('img')
        for k in range(len(poster_link)):
            alt = data_df["片名"][i] + "劇照"
            match = poster_link[k]['alt']
            # print(f'match = {match}, alt = {alt}, match == alt = {match[:3] == alt[:3]}')
            
            # 有些alt的命名很偷懶，會有標點符號全半型的問題 或是 簡寫片名的問題，因此，相對應只比對前三個字元 或 後四個字元(最後兩個字元必為劇照)
            if match[:3] == alt[:3] or match[-4:] == alt[-4:]:  
                poster_url[i].append(poster_link[k]['data-src']) 

    data_df['劇照'] = poster_url

    return data_df

# df = crawling("https://movies.yahoo.com.tw/chart.html")


