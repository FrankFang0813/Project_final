import pymongo
import pymysql

def connect_to_mysql(user,passwd,db):
    # 設定資料庫連線資訊
    db_setting = {
        "host" : 'localhost',
        "port" : 3306,
        "user" : user,
        "passwd" : passwd,
        "db" : db,
        "charset" : 'utf8mb4'
        }
    conn = pymysql.connect(**db_setting)
    print("Mysql connect")
    return conn
def mysql_select_data():
    area = input('地區:')
    year = input('年資:')
    category = input('種類:')
    conn = connect_to_mysql('root','frank0813','topic_104')  # 連接資料庫
    cursor = conn.cursor()

    dic = {'work_area_clean': f'%{area}%'
           ,'Work_exp': f'%{year}%'
           ,'jobCat_main': f'%{category}%'}
    # for i in sorted(dic.items(), key=lambda x: x[1], reverse=True):
    # a = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    sql = f"""
    SELECT * FROM job_104 
    where work_area_clean like '{dic['work_area_clean']}' 
    and Work_exp like '{dic['Work_exp']}' 
    and jobCat_main like '{dic['jobCat_main']}'; 
    """

    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    conn.close()

mysql_select_data()