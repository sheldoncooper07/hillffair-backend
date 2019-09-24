from flask import Flask, render_template, request, redirect, url_for, session, logging
import pymysql.cursors
import numpy

# add following code to use in app.py
# app.add_url_rule('/facesmash', 'faceSmash', faceSmash, methods=['GET', 'POST'])


def faceSmash():
        faceSmash_tableName = "profile"
        faceSmash_league_diff = 5
        faceSmash_ratingIncrease = 1
        faceSmash_request = '/faceSmash'

        connection = pymysql.connect(host="127.0.0.1", user="moulik", password="bigbang2",
                                     db="hillffair", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

        with connection.cursor() as cursor:
                #for GET requests
                if request.method == "GET":
                        #generating gender
                        gen = numpy.random.randint(0, 2)
                        # generating the range of users to be considered
                        cursor.execute("select min(rating), max(rating) from " +
                                       str(faceSmash_tableName)+" where gender = '"+str(gen)+"';")
                        league = cursor.fetchone()
                        minVal = league["min(rating)"]
                        maxVal = league["max(rating)"]
                        league = numpy.random.randint(minVal, maxVal+1)
                        #selecting users from the given range
                        cursor.execute("select * from "+str(faceSmash_tableName)+" where rating >= "+str(league-faceSmash_league_diff)+" AND rating <=" + str(league+faceSmash_league_diff)+" AND gender = '"+str(gen)+"'"
                                       "order by rand();")
                        ans = cursor.fetchall()
                        checks = 0
                        while(len(ans) < 2):
                                checks += 1
                                if checks == 10:
                                        break
                                gen = numpy.random.randint(0, 2)
                                cursor.execute(
                                    "select min(rating), max(rating) from "+str(faceSmash_tableName)+" where gender = '"+str(gen)+"';")
                                league = cursor.fetchone()
                                minVal = league["min(rating)"]
                                maxVal = league["max(rating)"]
                                league = numpy.random.randint(minVal, maxVal+1)
                                cursor.execute("select * from "+str(faceSmash_tableName)+" where rating >= "+str(league-faceSmash_league_diff)+" AND rating <=" + str(league+faceSmash_league_diff)+" AND gender = '"+str(gen)+"'"
                                               "order by rand();")
                                ans = cursor.fetchall()
                        # final failsafe
                        if checks == 10:
                                gen = numpy.random.randint(0, 2)
                                cursor.execute(
                                    "select * from "+str(faceSmash_tableName)+" where  gender = '"+str(gen)+"'order by rand();")
                                ans = cursor.fetchall()
                        return "[{image_url:"+str(ans[0]["url"])+"},{image_url:"+str(ans[1]["url"])+"}]"
                # for POST requests
                elif request.method == "POST":
                        imgURL = request.args.get('image_url')
                        # incrementing the rating of winning user
                        cursor.execute("update "+str(faceSmash_tableName)+" set rating = rating + "+str(
                            faceSmash_ratingIncrease)+" where url = '"+str(imgURL)+"';")
                        return redirect(faceSmash_request)
