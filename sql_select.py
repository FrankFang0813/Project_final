import pymongo
import pymysql
import time
import json
import pprint
import pandas as pd

def connect_to_mysql():
    # 設定資料庫連線資訊
    db_setting = {
        "host" : '192.168.1.106',
        "port" : 3306,
        "user" : 'root',
        "passwd" : 'root',
        "db" : "topic_104",
        "charset" : 'utf8mb4'
        }
# 建立連線
    conn = pymysql.connect(**db_setting)
    print('Successfully connected to DB : {} !'.format(db_setting["db"]))
    return conn

def data_find():
    # 游標執行(insert指令,資料)
    conn = connect_to_mysql()
    # cursor = conn.cursor()

    select_sql = '''
    select * from job_104
    where Job_Name like "%資料科學家%"
    '''

    #可直接取出資料成dataframe
    a = pd.read_sql(select_sql,con = conn)
    # cursor.execute(select_sql)
    # select要搭配cursor.fetchone() 使用
    # 多次使用cursor.fetchone()會從第一筆開始找,1.2.3......以此類推
    # a = cursor.fetchall()
    # b = cursor.fetchone()
    # 也可使用cursor.fetchall() 一次全部取出
    #allll = cursor.fetchall()
    # conn.commit()
    pprint.pprint(a)
    print("===================================================")
    # pprint.pprint(b)
    # 游標關閉
    # cursor.close()
    # 中斷連線
    # conn.close()

if __name__ == '__main__':
    connect_to_mysql()
    data_find()