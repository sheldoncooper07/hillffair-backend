from flask import Flask, request, Response
from pymysql import cursors
import json

def rewards(connection):
    fbID = request.form.get("firebase_id")
    subCnd = request.form.get("sub_candies")
    with connection.cursor() as cursor:
        cursor.execute("SELECT points from profile where firebase_id = '{}'".format(fbID))
        candies = cursor.fetchone()
        if cursor.rowcount==0:
            return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json", status = 400)
        candies = candies["points"]
        if(int(candies) < int(subCnd)):
            return Response(json.dumps({"status": "failure", "status_code": "200"}), mimetype="application/json", status=200)
        cursor.execute("UPDATE profile SET points = points - {} WHERE firebase_id = '{}'".format(subCnd,fbID))
        connection.commit()
        return Response(json.dumps({"status": "success", "status_code": "200"}), mimetype="application/json", status=200)
