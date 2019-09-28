from flask import Flask , request, Response
import pymysql.cursors
import json


# add following code to use in app.py
# app.add_url_rule('/facesmash', 'faceSmash.faceSmash', faceSmash.faceSmash, methods=['GET', 'POST'], defaults = {"connection":connection})


def ELO_Change(RWin, RLose):
        x = 400
        y = 30
        eA = 1/(1+10**((RLose-RWin)/x))
        eB = 1-eA
        return RWin+y*(1-eA), RLose+y*(0-eB)

def faceSmash(connection):
        faceSmash_tableName = "profile"
        faceSmash_league_diff = 5
        faceSmash_ratingIncrease = 1


        with connection.cursor() as cursor:
                #for GET requests
                if request.method == "GET":
                        cursor.execute("SELECT name, firebase_id, url, gender, rating FROM profile ORDER BY rating DESC")
                        if cursor.rowcount == 0:
                                return Response({"status":"fail"},mimetype = 'application/json')
                        return Response(json.dumps(cursor.fetchall()),mimetype=("application/json"))
                # for POST requests
                elif request.method == "POST":
                        UID = request.form.get('UID')
                        ID1 = request.form.get('ID1')
                        ID2 = request.form.get('ID2')
                        WID = request.form.get('WID')
                        # incrementing the rating of winning user
                        
                        cursor.execute("select rating from profile where firebase_id = {}".format(WID))
                        if cursor.rowcount==0:
                                return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
                        rA = cursor.fetchone()
                        rA = rA["rating"]
                        LID=ID2
                        if ID2==WID:
                                LID=ID1
                        cursor.execute("select rating from profile where firebase_id = {}".format(LID))
                        if cursor.rowcount==0:
                                return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
                        rB = cursor.fetchone()
                        rB = rB["rating"]
                        rA,rB = ELO_Change(rA,rB)
                        query = "UPDATE profile SET rating = {} where firebase_id = {}".format(round(rA),WID)
                        cursor.execute(query)
                        connection.commit()
                        if cursor.rowcount == 0:
                                return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
                        query = "UPDATE profile SET rating = {} where firebase_id = {}".format(round(rB),LID)
                        cursor.execute(query)
                        connection.commit()
                        if cursor.rowcount == 0:
                                return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
                        # insertion to queue table
                        if cursor.rowcount == 0:
                                return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
                        return Response(json.dumps({"status": "success", "status_code": "200"}),mimetype="application/json",status=200)
