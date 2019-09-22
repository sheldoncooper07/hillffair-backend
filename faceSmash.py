from flask import Flask, render_template, request, redirect, url_for, session, logging
import pymysql.cursors
import numpy
import values

# add following code to use in app.py
# app.add_url_rule(values.faceSmash_request, 'faceSmash', faceSmash, methods=['GET', 'POST'])

def faceSmash():
        connection = pymysql.connect(host=values.sqlHost, user=values.sqlUser, password=values.sqlPass,
                                     db=values.dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

        with connection.cursor() as cursor:
                if request.method == "GET":
                        gen = numpy.random.random()
                        if(gen<.5):
                                gen = "MALE"
                        else :
                                gen = "FEMALE"
                        cursor.execute("select min(rating), max(rating) from "+values.faceSmash_tableName+" where gender = '"+gen+"';")
                        league = cursor.fetchone()
                        minVal = league["min(rating)"]
                        maxVal = league["max(rating)"]
                        league = numpy.random.randint(minVal,maxVal)
                        cursor.execute("select * from "+values.faceSmash_tableName+" where rating >= "+str(league-values.faceSmash_league_diff)+" AND rating <" +str(league+values.faceSmash_league_diff)+" AND gender = '"+gen+"'"
                        "order by rand();")
                        ans = cursor.fetchall()
                        while(len(ans)<2):
                                gen = numpy.random.randint(0,2)
                                if(gen == 0):
                                        gen = "MALE"
                                else:
                                        gen = "FEMALE"
                                cursor.execute("select min(rating), max(rating) from "+values.faceSmash_tableName+" where gender = '"+gen+"';")
                                league = cursor.fetchone()
                                minVal = league["min(rating)"]
                                maxVal = league["max(rating)"]
                                league = numpy.random.randint(minVal,maxVal)
                                cursor.execute("select * from "+values.faceSmash_tableName+" where rating >= "+str(league-values.faceSmash_league_diff)+" AND rating <" +str(league+values.faceSmash_league_diff)+" AND gender = '"+gen+"'"
                                "order by rand();")
                                ans = cursor.fetchall()
                        return "[{image_url:"+ans[0]["imageID"]+"},{image_url:"+ans[1]["imageID"]+"}]"
                else:
                        imgURL = request.args.get('image_url')
                        cursor.execute("update "+values.faceSmash_tableName+" set rating = rating + 1 where imageID = '"+str(imgURL)+"';")
                        return redirect(values.faceSmash_request)
