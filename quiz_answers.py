from flask import Flask, request
from pymysql import cursors

def javaHashMapStrToJson(data):
    data = data.replace(',', '}, {')
    data = data.replace('=',',')
    data = data.replace("'",'"')
    data = '['+data+']'
    data = eval(data)
    data = sorted(data,key = lambda i:i['id'])
    return data

def answers(connection):
    with connection.cursor() as cursor:
        id = request.form.get("firebase_id")
        data = request.form.get("answers")
        data = javaHashMapStrToJson(data)
        score = 0
        id = 0
        query = "select @rownum := @rownum+1 As rank, quiz.* from quiz, (select @rownum := 0) r where id = ".format(data[id]["id"])
        for i in range(len(data)):
            query += " {} or id = ".format(data[id]["id"])
            id+=1
        id = 0
        query = query[:-9]
        print(query)
        cursor.execute(query)
        ans = cursor.fetchall()
        for i in range(len(data)):
            qid = ans[id]["id"]
            print(int(ans[id]["ans"]), int(data[id]["ans"]))
            if(int(ans[id]["ans"])==int(data[id]["ans"])):
                score+=1
            id+=1
    return '{"Score":"'+str(score)+'"}'
