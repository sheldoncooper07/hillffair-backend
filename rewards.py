from flask import Flask, request, Response
from pymysql import cursors

def rewards(connection):
    fbID = request.form.get("firebaseid")
    print(fbID)
    subCnd = request.form.get("sub_candies")
    with connection.cursor() as cursor:
        cursor.execute("SELECT points from profile where firebase_id = {}".format(fbID))
        candies = cursor.fetchone()
        if cursor.rowcount==0:
            return Response({"status":"fail"},mimetype="application/json")
        candies = candies["points"]
        print(candies)
        print(subCnd)
        if(int(candies)<int(subCnd)):
            return {"status":"fail"}
        print("UPDATE profile SET points = points - {} WHERE firebase_id = '{}'".format((subCnd), fbID))
        cursor.execute("UPDATE profile SET points = points - {} WHERE firebase_id = '{}'".format((subCnd),fbID))
        connection.commit()
        if cursor.rowcount==0:
            return Response({"status":"fail"},mimetype="application/json")
        return {"status":"success"}