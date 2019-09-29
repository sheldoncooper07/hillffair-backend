import rewards
from flask import Flask, request, jsonify, Response
from functools import wraps
import json, time
from datetime import datetime
import random
import pymysql.cursors
import base64
import faceSmash
app = Flask(__name__)
import faceSmash
import quiz_answers


global cursor

connection = pymysql.connect(host='127.0.0.1',
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
    #print("INSERT into wall VALUES(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    query = cursor.execute("INSERT into Wall VALUES(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    cursor.execute(query)
    connection.commit()
    return {'status': 'success',"status_code":200}


@app.route('/User', methods=['POST'])
def addUser():
    # try:
        fbID = request.form.get('firebase_id')
        cursor.execute("SELECT firebase_id FROM profile WHERE firebase_id = '{}'".format(fbID))
        if cursor.rowcount != 0:
            return Response(json.dumps({"status": "failure", "reason": "User already exists", "status_code": "400"}), mimetype="application/json",status = 400)
        name = request.form.get('name')
        gender = request.form.get('gender')
        if gender == "MALE":
            gender = 0
        else:
            gender = 1
        rollno = request.form.get('roll_number')
        branch = request.form.get('branch')
        mobile = request.form.get('mobile')
        referral = request.form.get('referral_friend')
        imgURL = "0"
        status = request.form.get('face_smash_status')
        if status != 0:
            imgURL = request.form.get('image_url')
        cursor.execute("SELECT * FROM profile;")
        cursor.execute("INSERT into profile VALUES('{FbID}','{roll}','{branch}','{mobile}','{name}',0,{gender},'{url}',1500,'{referral}', '0')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
        connection.commit()
        return Response(json.dumps({"status": "success", "status_code": "200"}),mimetype = "application/json", status = 200)
    # except:
        return Response(json.dumps({"status": "failure", "reason": "Unknown", "status_code": "400"}), mimetype="application/json")

@app.route('/User/<fbID>',methods=["GET"])
def getUserProfile(fbID):
    cursor.execute("SELECT 'success' AS 'status', '200' AS 'status_code', firebase_id AS firebase_id, rollno AS 'roll_number', branch, mobile, points AS 'candies', referral_friend,name,gender,url AS image_url, face_smash_status FROM profile WHERE firebase_id = '{fbID}'".format(fbID=fbID))
    if cursor.rowcount == 0:
            return Response(json.dumps({"status":"failure","status_code":"400"}), mimetype="application/json",status = 400)
    data = cursor.fetchone()
    return Response(json.dumps(data),mimetype="application/json",status =200)

@app.route('/User/Update', methods = ["POST"])
def updateUser():
    fbID = request.form.get("firebase_id")
    if fbID == None :
        return Response(json.dumps({"status": "failure", "status_code": "400"}),mimetype="application/json",status=400)
    imgURL = request.form.get("image_url")
    cursor.execute("UPDATE profile SET url = '{}', face_smash_status = 1 WHERE firebase_id ='{}'".format(imgURL,fbID))
    connection.commit()
    return Response(json.dumps({"status":"success", "status_code":"200"}),mimetype="application/json",status=200)


@app.route('/profile', methods=['POST'])
def addUserProfile():
    fbID = request.form.get('firebase_id')
    rollno = request.form.get('roll number')
    branch = request.form.get('branch')
    mobile = request.form.get('mobile')
    name = request.form.get('name')
    gender = request.form.get('gender')
    imgURL = request.form.get('image_url')
    referral = request.form.get('referral_friend')
    print("INSERT INTO profile VALUES('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    cursor.execute("INSERT INTO profile VALUES('{FbID}','{roll}','{branch}','{mobile}','{name}',0,'{gender}','{url}',0,'{referral}')".format(FbID=fbID,roll=rollno,branch=branch,mobile=mobile,name=name,gender=gender,url=imgURL,referral = referral))
    connection.commit()
    return {"status_code":200,"status":"success"}

@app.route('/profile/',methods=["GET"])
def getUser():
    fbID = request.form.get('firebase_id')
    cursor.execute("select firebase_id AS firebase_id, rollno AS 'roll number', branch, mobile, referral_friend,name,gender,url AS image_url FROM profile WHERE firebase_id = '{fbID}'".format(fbID=fbID))
    data = cursor.fetchone()
    if(data):
        return data
    else:
        return {"status":"User not found"}

@app.route('/like',methods=['POST'])
def like():
    firebase_id=request.form['firebase_id']
    post_id=request.form['post_id']

    query = "SELECT * FROM likes WHERE firebase_id='{}' AND post={}".format(firebase_id, post_id)
    cursor.execute(query)
    if cursor.rowcount==0:
        try:
            print("deb")
            cursor.execute("INSERT INTO likes VALUES(NULL,{},'{}')".format(post_id,firebase_id))
            connection.commit()
            cursor.execute("SELECT firebase_id FROM wall WHERE id={}".format(post_id))
            print("deb")
            fbID = cursor.fetchone().get("firebase_id")
            cursor.execute("UPDATE wall SET likes = likes+1 WHERE firebase_id = '{}' AND id = {}".format(firebase_id,post_id))
            print("deb")
            connection.commit()
            print(
            	"UPDATE profile SET points=points+1 WHERE firebase_id = '{}'".format(fbID))
            cursor.execute("UPDATE profile SET points=points+1 WHERE firebase_id = '{}'".format(fbID))
            print("deb")
            connection.commit()
            print(cursor.rowcount)
            if cursor.rowcount == 0:
                return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json",status=400)
            return Response(json.dumps({"status":"success", "status_code":"200"}), mimetype = "application/json", status = 200)
        except:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json", status=400)
    return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
    
@app.route('/unlike',methods=["POST"])
def unlike():
    firebase_id = request.form["firebase_id"]
    post_id = request.form["post_id"]
    cursor.execute("SELECT * FROM likes WHERE firebase_id='{}' AND post={}".format(firebase_id,post_id))
    if cursor.rowcount == 0:
        return Response(json.dumps({"status":"failure", "status_code":"400"}),mimetype="application/json",status=400)
    cursor.execute("DELETE FROM likes WHERE firebase_id='{}' AND post={}".format(firebase_id,post_id))
    connection.commit()
    cursor.execute("SELECT firebase_id FROM wall WHERE id = {}".format(post_id))
    fbID = cursor.fetchone()["firebase_id"]
    cursor.execute("UPDATE profile SET points = points-1 WHERE firebase_id = '{}'".format(fbID))
    connection.commit()
    cursor.execute("UPDATE wall SET likes = likes-1 WHERE firebase_id = '{}' AND id = {}".format(firebase_id,post_id))
    connection.commit()
    return Response(json.dumps({"status": "success", "status_code": "200"}), mimetype="application/json",status=200)



app.add_url_rule('/faceSmash', 'faceSmash.faceSmash', faceSmash.faceSmash, methods=['GET', 'POST'], defaults = {"connection":connection})
app.add_url_rule('/quiz/answers','quiz_answers.answers',quiz_answers.answers,methods=['POST'],defaults={"connection":connection})
app.add_url_rule('/reward','rewards.rewards', rewards.rewards, methods = ["POST"],defaults = {"connection":connection})

@app.route('/quiz/questions',methods=['POST'])
def quiz():
    category=request.form.get("category")
    query = "SELECT id,ques,option1,option2,option3,option4 FROM quiz WHERE category={} ORDER BY RAND() LIMIT 10 ".format(category)
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype = "application/json",status=400)
    questions=cursor.fetchall()
    ans = {}
    ans["status"] = "success"
    ans["status_code"] = "200"
    ans["questions"] = questions
    return Response(json.dumps(ans),mimetype="application/json",status=200)

@app.route('/profile',methods=['POST'])
def profile():
    firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url=request.form.firebase_id,request.form.rollno,request.form.branch,request.form.mobile,request.form.referl_friend,request.form.name,request.form.gender,request.form.image_url
    query="INSERT INTO profile VALUES(firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url)"
    cursor.execute(query)
    connection.commit()
    return {"status_code":200}



@app.route('/Club_info' ,methods=['GET'])
def club():
    query="SELECT name AS club_name, logo AS image_url, info AS description FROM clubs"
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json", status = 400)
    details=cursor.fetchall()
    ans = {}
    ans["status"] = "success"
    ans["status_code"]="200"
    ans["clubs"]=details
    return Response(json.dumps(ans),mimetype="application/json",status=200)


@app.route('/core_team/' ,methods=['GET'])
def core():
    query="SELECT name, profile_pic AS image_url, position FROM coreteam"
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json", status = 400)
    core_details=cursor.fetchall()
    ans = {}
    ans["status"]="success"
    ans["status_code"]="200"
    ans["members"]=core_details
    return Response(json.dumps(ans),mimetype="application/json",status=200)

@app.route('/sponsors')
def sponsors():
    query="SELECT sponsor_name, sponsor_logo AS image_url, sponsor_info FROM sponsors AS sponsor"
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json",status = 400)
    sponsor=cursor.fetchall()
    ans = {}
    ans["status"]="success"
    ans["status_code"]="200"
    ans["sponsors"]=sponsor
    return Response(json.dumps(ans),mimetype="application/json", status = 200)


@app.route('/leaderboard')
def leaderboard():
    query="SELECT name AS Name, points AS candies, gender AS Gender FROM profile order by points DESC"
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json", status = 400)
    details=cursor.fetchall()
    ans = {}
    ans["status"]="success"
    ans["status_code"]="200"
    ans["leaderboard"]=details
    return Response(json.dumps(ans),mimetype="application/json",status=200)



@app.route('/feed',methods=['POST'])
def feed():
    firebase_id=request.form['firebase_id']
    url=request.form['image_url']
    try:
        query="INSERT INTO wall VALUES(Null,'{}',0,'{}')".format(firebase_id,url)
        cursor.execute(query)
        connection.commit()
    except:
        return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype = 'application/json', status = 400)
    return Response(json.dumps({"status": "success", "status_code": "200", }),mimetype = "application/json", status = 200)

@app.route('/feed/<page_index>/<firebase_id>', methods=['GET'])
def feedg(page_index, firebase_id):
    page_index = int(page_index)
    page_index1 = (page_index-1)*10
    page_index1 = str(page_index1)
    # syntax of limit is : LIMIT startingIdx,number of elements to be taken;
    query="SELECT * FROM wall ORDER BY ID DESC LIMIT {}, 10".format(page_index1)
    ret_arr=[]
    cursor.execute(query)
    if cursor.rowcount == 0:
            return Response(json.dumps({"status": "failure", "status_code": "400"}), mimetype="application/json", status = 400)
    photos=cursor.fetchall()
    for i in range(0, len(photos)):
        print(photos[i])
        cursor.execute("SELECT * FROM likes WHERE firebase_id= '{}' AND post={}".format(firebase_id,page_index))
        like = 1
        if cursor.rowcount==0:
            like = 0
        count = photos[i]["likes"]
        ret_arr.append({"post_id":photos[i]["id"],"image_url":photos[i]['url'], "likes":count,"liked":like})
    ans = {}
    ans["status"] = "success"
    ans["status_code"] = "200"
    ans["feed"] = ret_arr
    return Response(json.dumps(ans),mimetype="application/json", status = 200)




# @app.route('/rewards',methods=['POST'])
# # def rewards():
# #     firebase_id=request.form.firebase_id
# #     candies=request.form.sub_candies
# #     query="UPDATE profile SET points=points-'"+candies+"' WHERE firebase_id='"+firebase_id+"'"
# #     return {"status_code":200}# not in docs


# @app.route('/rewards',methods=['POST'])
# def rewards():
#     firebase_id=request.form.get('firebase_id')
#     candies=request.form.get('sub_candies')
#     print(firebase_id,candies)
#     query = "SELECT points FROM profile WHERE firebase_id = "+ firebase_id
#     cursor.execute(query)
#     points = cursor.fetchall()
#     print(points)
#     if points>=candies:
#         query="UPDATE profile SET points = points -"+candies+" WHERE firebase_id="+firebase_id
#         cursor.execute(query)
#         return jsonify({"status_code":200})# not in docs
#     else:
#         return jsonify({"status_code":404})



@app.route('/schedule', methods = ["GET", "POST"])
def schedule():
    if request.method == "GET":
        cursor.execute("SELECT event_id, club_name, event_name, date(time) AS date, time(time) AS time FROM schedule INNER JOIN clubs ON clubs.id = schedule.club_id")
        if cursor.rowcount == 0:
            return Response(json.dumps({"status":"failure", "status_code":"200"}),content_type = "application/json", status = 200)
        ans = {}
        ans["status"] = "success"
        ans["status_code"] = "200"
        ans["schedule"] = cursor.fetchall()
        for i in range(cursor.rowcount):
            ans["schedule"][i]["time"] = str(ans["schedule"][i]["time"])
            ans["schedule"][i]["date"] = str(ans["schedule"][i]["date"])
        return Response(json.dumps(ans),mimetype = "application/json", status = 200)
    elif request.method == "POST":
        club_name = request.form.get("club_name")
        event_name = request.form.get("event_name")
        time = request.form.get("time")
        try:
            cursor.execute("INSERT INTO schedule VALUES(Null,(SELECT id FROM clubs WHERE name = '{club_name}'), '{club_name}', '{event_name}', '{time}')".format(club_name = club_name, event_name = event_name, time = time))
            connection.commit()
            return Response(json.dumps({"status": "success", "status_code": "200"}), mimetype = "application/json", status=200)
        except:
            return Response(json.dumps({"status":"failure","status_code":"400"}),mimetype="application/json", status=  400)

@app.route("/schedule/<club_name>")
def ClubSchedule(club_name):
    cursor.execute("SELECT event_id, club_name, event_name, date(time) AS date, time(time) AS time FROM schedule INNER JOIN clubs ON clubs.id = schedule.club_id where club_name = '{}'".format(club_name))
    if cursor.rowcount == 0:
        return Response(json.dumps({"status":"failure", "status_code":"200"}),content_type = "application/json", status = 200)
    ans = {}
    ans["status"] = "success"
    ans["status_code"] = "200"
    ans["schedule"] = cursor.fetchall()
    for i in range(cursor.rowcount):
        ans["schedule"][i]["time"] = str(ans["schedule"][i]["time"])
        ans["schedule"][i]["date"] = str(ans["schedule"][i]["date"])
    return Response(json.dumps(ans), mimetype="application/json", status=200)

    

if __name__ == '__main__':
    app.run(debug = True, host='127.0.0.1')
