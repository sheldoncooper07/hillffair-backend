from flask import Flask, request, jsonify
from functools import wraps
import json, time
from datetime import datetime
import random
import pymysql.cursors
import base64
import faceSmash
app = Flask(__name__)
import faceSmash as faceSmash

global cursor

connection = pymysql.connect(host='localhost',
                                         user='hillffair',
                                         password='1qaz2wsx',
                                         db='hillffair',
                                         cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


@app.route('/makesponsors',methods=['POST'])
def make():
	query="INSERT INTO sponsor VALUES ('app team','google.com','info')"
	cursor.execute(query)
	connection.commit()
	return {"status_code":200}

@app.route('/postwall/<rollno>/<imageurl>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "s": 2}]
def postwall(rollno,imageurl):

    imageurl=imageurl
    #print("INSERT into wall values(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    query = cursor.execute("INSERT into Wall values(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    cursor.execute(query);
    connection.commit();
    return {'status': 'success',"status_code":200}


@app.route('/User/', methods=['POST'])
def addUser():
    fbID = request.form.get('Firebaseid')
    rollno = request.form.get('roll number')
    branch = request.form.get('branch')
    mobile = request.form.get('mobile')
    name = request.form.get('name')
    gender = request.form.get('gender')
    imgURL = request.form.get('image_url')
    referral = request.form.get('referral_friend')
    print("insert into profile values('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    cursor.execute("insert into profile values('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    connection.commit()
    return {"status":"success"}

@app.route('/User/<fbID>',methods=["GET"])
def getUserProfile(fbID):
    cursor.execute("select firebase_id as Firebaseid, rollno as 'roll number', branch, mobile, referral_friend,name,gender,url as image_url from profile where firebase_id = '{fbID}'".format(fbID=fbID))
    data = cursor.fetchone()
    return data

@app.route('/profile', methods=['POST'])
def addUserProfile():
    fbID = request.form.get('Firebaseid')
    rollno = request.form.get('roll number')
    branch = request.form.get('branch')
    mobile = request.form.get('mobile')
    name = request.form.get('name')
    gender = request.form.get('gender')
    imgURL = request.form.get('image_url')
    referral = request.form.get('referral_friend')
    print("insert into profile values('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    cursor.execute("insert into profile values('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    connection.commit()
    return {"status_code":200,"status":"success"}

@app.route('/profile/',methods=["GET"])
def getUser():
    fbID = request.form.get('firebaseid')
    cursor.execute("select firebase_id as Firebaseid, rollno as 'roll number', branch, mobile, referral_friend,name,gender,url as image_url from profile where firebase_id = '{fbID}'".format(fbID=fbID))
    data = cursor.fetchone()
    if(data):
        return data
    else:
        return {"status":"User not found"}

@app.route('/like',methods=['POST'])
def like():
    firebase_id=request.form['firebase_id']
    image_url=request.form['image_url']        #use?

    query="UPDATE wall SET likes=likes+1 WHERE firebase_id='"+firebase_id+"'"
    cursor.execute(query)
    connection.commit()

    query="SELECT firebase_id as fid FROM wall WHERE url='"+image_url+"'"
    cursor.execute(query)
    fid=cursor.fetchone()
    #print(fid)
    fid2 = str(fid['fid'])
    q="UPDATE profile SET points=points+1 WHERE firebase_id='"+fid2+"'"
    cursor.execute(q)
    connection.commit()
    
    return jsonify({"status_code":200})
    
    
app.add_url_rule('/faceSmash', 'faceSmash.faceSmash', faceSmash.faceSmash, methods=['GET', 'POST'], defaults = {"connection":connection})

@app.route('/quiz/questions',methods=['POST'])
def quiz():
    category=request.form.get('category')
    query="SELECT id,ques,option1,option2,option3,option4 FROM quiz WHERE category={} ORDER BY RAND() LIMIT 10".format(category)
    cursor.execute(query)
    questions=cursor.fetchall()
    return json.dumps(questions)
    #random on client side'

@app.route('/quiz/answers',methods=['POST'])
def quiz_answers():
    points = 0
    firebase_id = request.form.get('firebase_id')
    answers = request.form.get('answers')

    for in range(0, len(answers)):
        cursor.execute("SELECT answer FROM quiz WHERE id='" + answers[i]['id']+"'")
        answer = cursor.fetchone()
        if answers[i].answer == answer:
            points = points+1
    cursor.execute("UPDATE profile SET points = points + '" + points + "' WHERE ID= '" + firebase_id + "'")
    return points
    
@app.route('/profile',methods=['POST'])
def profile():
    firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url=request.form.firebase_id,request.form.rollno,request.form.branch,request.form.mobile,request.form.referl_friend,request.form.name,request.form.gender,request.form.image_url
    query="INSERT INTO profile VALUES(firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url"
    cursor.execute(query)
    connection.commit()
    return {"status_code":200}
    


@app.route('/club_info' ,methods=['GET'])
def club():
    query="SELECT * from clubs"
    cursor.execute(query)
    details=cursor.fetchall()
    return json.dumps(details)


@app.route('/core_team/' ,methods=['GET'])  
def core():
    query="SELECT name, profile_pic as image_url, position from coreteam"
    cursor.execute(query)
    core_details=cursor.fetchall()
    return json.dumps(core_details)
    
    
    
    
@app.route('/sponsors')
def sponsors():
    query="SELECT * from sponsors as sponsor"
    cursor.execute(query)
    sponsor=cursor.fetchall()
    return json.dumps(sponsor)

    
@app.route('/leaderboard')
def leaderboard():
    query="SELECT name as Name, points as candies, gender as Gender from profile order by points DESC"
    cursor.execute(query)
    details=cursor.fetchall()

    return json.dumps(details)



@app.route('/feed',methods=['POST'])
def feed():
    firebase_id=request.form['firebase_id']
    url=request.form['image_url']
    query="INSERT INTO wall (firebase_id, likes, url) VALUES('"+firebase_id+"',0,'"+url+"')"
    cursor.execute(query)
    connection.commit()
    return jsonify({"status_code":200})

@app.route('/feed/<page_index>/<firebase_id>', methods=['GET'])
def feedg(page_index, firebase_id):
    page_index = (int)(page_index)
    page_index1 = (page_index-1)*10+1
    page_index2 = (page_index*10)
    page_index1 = str(page_index1)
    page_index2 = str(page_index2)
    query="SELECT * FROM wall ORDER BY ID DESC LIMIT "+ page_index1 +" , "+ page_index2
    ret_arr=[]
    cursor.execute(query)
    photos=cursor.fetchall()
    #print(photos[0])
    for i in range(0, len(photos)):
        print(photos[i])
        cursor.execute("SELECT * FROM likes WHERE firebase_id=" + str(firebase_id) + " AND post="+ str(photos[i]['id'])) 
        like=cursor.fetchone()
        if(like):
            q="SELECT COUNT(*) FROM likes where post="+str(photos[i]['id'])
            cursor.execute(q)
            count=len(cursor.fetchall())
            ret_arr.append({"image_url":photos[i]['url'], "likes":count,"liked":1})
        else:
        	q="SELECT COUNT(*) FROM likes where post="+str(photos[i]['id'])
        	cursor.execute(q)
        	count=len(cursor.fetchall())
	        ret_arr.append({"image_url":photos[i]['url'], "likes":count,"liked":0})
    return json.dumps(ret_arr)

    
    

# @app.route('/rewards',methods=['POST'])
# # def rewards():
# #     firebase_id=request.form.firebase_id
# #     candies=request.form.sub_candies
# #     query="UPDATE profile SET points=points-'"+candies+"' WHERE firebase_id='"+firebase_id+"'"
# #     return {"status_code":200}# not in docs


@app.route('/rewards',methods=['POST'])
def rewards():
    firebase_id=request.form.get('firebase_id')
    candies=request.form.get('sub_candies')
    print(firebase_id,candies)
    query = "SELECT points from profile WHERE firebase_id = "+ firebase_id
    cursor.execute(query)
    points = cursor.fetchall()
    print(points)
    if points>=candies:
        query="UPDATE profile SET points = points -"+candies+" WHERE firebase_id="+firebase_id
        cursor.execute(query)
        return jsonify({"status_code":200})# not in docs
    else:
        return jsonify({"status_code":404})



@app.route('/getschedule')
def getschedule():
    query = cursor.execute("SELECT name as club_name, event_id,event_name,event_time,club_logo FROM events,clubs WHERE events.club_id=clubs.id")
    result = cursor.fetchall()
    #for x in result:
        #x["event_time"] = x["event_time"].timestamp()
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
