from flask import Flask, request, Response
from pymysql import cursors
import json

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
        try:
            data = javaHashMapStrToJson(data)
        except:
            return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status = 400)
        score = 0
        id = 0
        query = "select * from quiz where id = ".format(data[id]["id"])
        for i in range(len(data)):
            query += " {} or id = ".format(data[id]["id"])
            id+=1
        id = 0
        query = query[:-9]
        cursor.execute(query)
        if cursor.rowcount==0:
            return Response({"status":"fail"},mimetype="application/json")
        ans = cursor.fetchall()
        for i in range(len(data)):
            qid = ans[id]["id"]
            if(int(ans[id]["ans"])==int(data[id]["ans"])):
                score+=1
            id+=1
    return Response(json.dumps({"status": "success", "status_code": "200", "score": score}),mimetype = "application/json",status = 200)
