import pymongo
from pymongo import MongoClient
import json
import os


# 開啟json檔
def open_json_file(CACHE_FNAME):


    try:
        cache_file = open('./jobclean/'+CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        # print(type(cache_contents))
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
        # CACHE_DICTION才是dict格式
        return CACHE_DICTION

    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

# 跟mongodb建立連線
def mongo_connect_build(db_name, col_name):
    global mycol
    client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")  # 跟mongodb建立連

    db = client[db_name]  # 選擇使用的db,不存在則會在資料輸入時自動建立
    mycol = db[col_name]  # 選擇collection,不存在則會在資料輸入時自動建立



# 輸入資料
def data_insert(CACHE_DICTION):

    # 輸入json轉成字典的變數名稱
    # 若字典裡values為空值,則跳過
    # if len(list(CACHE_DICTION.values())[0]) == 0:
    #     pass
    # else:
    mycol.insert_many(CACHE_DICTION)
    print(f'{CACHE_FNAME}輸入')

if __name__ == "__main__":

    mongo_connect_build('Topic_104','job_clean_test') # 連線mongodb


    # 班代設計程式爬下來之後,都會在data資料夾裡面,將各個檔案輸入到mongodb
    for CACHE_FNAME in os.listdir('./jobclean/'):

        CACHE_DICTION = open_json_file(CACHE_FNAME)

        data_insert(CACHE_DICTION)


