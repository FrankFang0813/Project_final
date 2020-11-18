import json
import pandas as pd


def open_json_file(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding='utf-8-sig')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents, encoding='utf-8-sig')
        cache_file.close()
        return CACHE_DICTION

    except:
        CACHE_DICTION = {}
        return CACHE_DICTION


def dump_json_file(query_dict, file_name):
    dumped_json_cache = json.dumps(query_dict)
    fw = open(file_name, "w")
    fw.write(dumped_json_cache)
    fw.close()
    print('successfully write down the file: ', file_name)

def map_Cat(job_Cat): # create a job mapping dictionary from Job category json file
    dict_Cat_map = {}

    for i in job_Cat:
        key = i['jobURL']
        value = (i['jobName_clean'], i['jobCat_main'], i['JobCat_layer'])
        if key not in dict_Cat_map.keys():
            dict_Cat_map[key] = value

    return dict_Cat_map

job_Cat = open_json_file('./test_jobClean.json')
job_Cat= map_Cat(job_Cat)

# print(len(job_Cat))

import pymongo


def mongo_connect_build(db_name, col_name):
    global mycol
    client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")  # 跟mongodb建立連

    db = client[db_name]  # 選擇使用的db,不存在則會在資料輸入時自動建立
    mycol = db[col_name]  # 選擇collection,不存在則會在資料輸入時自動建立

def data_find():
    # 尋找多筆資料
    return mycol.find()


def extract_job_title(job_data):
    lst_jobTile = []
    count_s = 0
    count_e = 0
    for i in job_data:

        try:
            job_URL = i['_id']  # get the "URL shortcut" of each job
            job_da = i['data']['data']
            job_header = job_da['header']
            job_jobdetail = job_da['jobDetail']
            job_condition = job_da['condition']

            dict_job = {}
            dict_job['jobURL'] = job_URL
            dict_job['jobName'] = job_header['jobName']
            dict_job['jobCategory'] = job_jobdetail['jobCategory'][0]['description']
            dict_job['companyName'] = job_header['custName']
            dict_job['appearDate'] = job_header['appearDate']
            dict_job['industry'] = job_da['industry']
            dict_job['addressRegion'] = job_jobdetail['addressRegion']
            dict_job['workExp'] = job_condition['workExp']
            dict_job['edu'] = job_condition['edu']

            dict_job['major'] = job_condition['major']
            dict_job['language'] = job_condition['language']
            job_specialty = []
            for spt in job_da['condition']['specialty']:
                job_specialty.append(spt['description'])
            dict_job['specialty'] = job_specialty
            dict_job['skill'] = job_condition['skill']
            dict_job['language'] = job_condition['language']
            dict_job['jobDescription'] = job_jobdetail['jobDescription']
            dict_job['certificate'] = job_condition['certificate']
            dict_job['jobType'] = job_jobdetail['jobType']
            dict_job['salary'] = job_jobdetail['salary']
            dict_job['salaryMin'] = job_jobdetail['salaryMin']
            dict_job['salaryMax'] = job_jobdetail['salaryMax']
            dict_job['other'] = job_condition['other']

            count_s += 1
            print('success')
            lst_jobTile.append(dict_job)
        except Exception as e:
            count_e += 1
            print(i['_id'], '有錯誤訊息:', e)

        print('成功:', count_s, " ", '錯誤:', count_e)
    return lst_jobTile

mongo_connect_build('Topic_104', 'NewJobs') # connect to mongoDB to get job data

job_data = data_find() # store the data
lst_jobTitle = extract_job_title(job_data) # extract job title

for i in lst_jobTitle[0:10]:
    print(i)
    print('-'*20)

key_lst = job_Cat.keys()
# Add new data from Job title data

dict_result = []
lst_URL = []

for i in lst_jobTitle:
    jobURL = i['jobURL']
    if (jobURL in key_lst) and (jobURL not in lst_URL):
        add_data = job_Cat[jobURL]
        i['jobName_clean'] = add_data[0]
        i['jobCat_main'] = add_data[1]
        i['JobCat_layer'] = add_data[2]

        lst_URL.append(jobURL)
        dict_result.append(i)
print(len(dict_result))

for page in range(0,14):
    if page == 13:
        dump_json_file(dict_result[page * 10000:-1], f'./jsondata/test_w_JobCat{page}.json')
    else:
        dump_json_file(dict_result[page*10000:page*10000+10000], f'./jsondata/test_w_JobCat{page}.json')
    print(f'JobCat{page} successfully write down')