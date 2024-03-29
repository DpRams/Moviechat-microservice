# Base image 是 python:3.7
FROM python:3.7

# requirement_main.txt 裡有我們需要的套件資訊， 
# 把他複製到container裡，路徑為 /app/requirement_main.txt
COPY ./requirement_main.txt /app/requirement_main.txt

# pip是python的套件管理工具
RUN pip install -r app/requirement_main.txt

# 切換到container裡的 /app 路徑作為工作目錄 
WORKDIR /app

#把本地端main資料夾複製到container的當前目錄(/app)，此處要先把程式分好才能定義下面指令
ADD . . 

# 5000是我們服務所在的port
EXPOSE 5000

# 在系統中加入一個新system user 和 group，名稱皆為appuser
RUN adduser --system --group --no-create-home appuser

# 把 /app 這個directory的擁有權指定給appuser
RUN chown appuser:appuser -R --verbose /app

# 把container的 user 轉到appuser
USER appuser
# CMD代表command，當你啟動這個container時，會預設執行這個指令
CMD ["python3","/app/app.py"]
