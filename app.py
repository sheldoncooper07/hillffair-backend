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
    #random on client side
    
@app.route('/profile',methods=['POST'])
def profile():
    firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url=request.form.firebase_id,request.form.rollno,request.form.branch,request.form.mobile,request.form.referl_friend,request.form.name,request.form.gender,request.form.image_url
    query="INSERT INTO profile VALUES(firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url"
    cursor.execute(query)
    connection.commit()
    return {"status_code":200}
    


@app.route('/club_info/<club_name>' ,methods=['GET'])
def club(club_name):
    query="SELECT * from clubs AS details where name='"+club_name+"'"
    cursor.execute(query)
    details=cursor.fetchone()
    return details


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
    firebase_id=request.form.firebase_id
    candies=request.form.sub_candies
    query="UPDATE profile SET points=points-'"+candies+"' WHERE firebase_id='"+firebase_id+"'"
    return {"status_code":200}# not in docs
    #---------------------------------------------------------------------------
    


@app.route('/getwall/<int:start>/<user_id>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "s": 2}]
def getwall(start,user_id):
    query = cursor.execute("SELECT w.id as id, p.name as name, p.id as rollno, (SELECT COUNT(*) FROM likes WHERE post_id=w.id) AS likes, (Select count(*) from likes where post_id=w.id AND profile_id='"+user_id+"') as liked, w.image_url, p.image_url AS profile_pic  FROM wall as w, profile as p WHERE p.id=w.profile_id ORDER BY w.time DESC")
    result = cursor.fetchall()
    return json.dumps(result)



@app.route('/getlike/<int:image_id>')
# Sample Response: {"likes": 2}
def getlike(image_id):
    query = cursor.execute("SELECT COUNT(*) AS likes FROM likes WHERE post_id="+str(image_id))
    result = cursor.fetchone()
    return result


@app.route('/postlike/<int:image_id>/<user_id>/<int:action>')
def postlike(image_id, user_id,action):
        if action==1:
            query = cursor.execute("INSERT INTO likes VALUES(NULL, '"+user_id+"', "+str(image_id)+")")
            if query:
                return {"status": "success"}
            else:
                return {"status": "fail"}
        else:
            query = cursor.execute("DELETE from likes where profile_id = '"+user_id+"' AND post_id = '"+str(image_id)+"'")
            if query:
                return {"status": "success"}
            else:
                return {"status": "fail"}

@app.route('/getleaderboard')
# Sample Response: [{"id": "17mi561", "name": "Daniyaal Khan", "score": 60.0}, {"id": "17mi560", "name": "Check", "score": 10.0}]
def getleaderboard():
    #print("SELECT p.id, p.name, p.image_url, ((SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=(UNIX_timestamp(timestamp(current_date))+19800)+(SELECT SUM(referal_score) FROM score WHERE profile_id=p.id)) as score FROM profile AS p ORDER BY score DESC LIMIT "+str(startfrom)+", "+str(startfrom+10))
    query = cursor.execute("SELECT p.id, p.name, p.image_url, ((SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=(UNIX_timestamp(timestamp(current_date))+19800) AND referal_score=0)) as score FROM profile AS p ORDER BY score DESC")
    result = cursor.fetchall()
    return json.dumps(result)


@app.route('/postpoint/<rollno>/<int:points>')
def postpoint(rollno, points):
    query = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"', "+str(points)+", "+str(time.time()+19800)+",0.0)")
    connection.commit()
    if query:
        return {"status": "success"}
    else:
        return {"status": "fail"}

@app.route('/getpoint/<rollno>')
def getpoint(rollno):
    query = cursor.execute("SELECT SUM(amount) AS points FROM score WHERE profile_id = '"+rollno+"' AND time>=(UNIX_timestamp(timestamp(current_date))+19800)")
    result = cursor.fetchone()
    return result


@app.route('/getschedule')
def getschedule():
    query = cursor.execute("SELECT name as club_name, event_id,event_name,event_time,club_logo FROM events,clubs WHERE events.club_id=clubs.id")
    result = cursor.fetchall()
    #for x in result:
        #x["event_time"] = x["event_time"].timestamp()
    return json.dumps(result)

@app.route('/posteventlike/<user_id>/<event_id>')
def posteventlike(user_id, event_id):
    userCheck = cursor.execute("SELECT * from profile where id = %s", (user_id))
    if userCheck == 0:
        return {"status": "No such user"}
    eventCheck = cursor.execute("SELECT * from events where event_id = %s", (event_id))
    if eventCheck == 0:
        return {"status": "No such event"}
    query = cursor.execute("SELECT * from event_likes where user_id = %s AND event_id = %s", (user_id, event_id))
    if query == 0:
        cursor.execute("INSERT INTO event_likes VALUES (NULL, %s, %s)", (event_id, user_id))
        connection.commit()
        return {"status": "success"}
    else:
        return {"status": "Already Liked"}

@app.route('/geteventlike/<event_id>')
def geteventlike(event_id):
    query = cursor.execute("SELECT COUNT(*) from event_likes where event_id = %s", event_id)
    result = cursor.fetchone()
    return {"likes": result["COUNT(*)"]}


	
	
@app.route('/getclubs')
def getclubs():
    query = cursor.execute("SELECT * FROM clubs")
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/getcoreteam')
def getcoreteam():
    query = cursor.execute("SELECT * FROM coreteam")
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/getsponsor')
def getsponsor():
    query = cursor.execute("SELECT * FROM sponsors")
    result = cursor.fetchall()
    return json.dumps(result)



@app.route('/getquiz')
def getquiz():
    # returns 10 random questions from category (day)%num_cat
    NUM_CATEGORIES = 7
    day_of_year = datetime.now().timetuple().tm_yday
    curr_cat = (day_of_year % NUM_CATEGORIES)
    query = cursor.execute("SELECT * FROM quiz WHERE category = %s",curr_cat)
    result = cursor.fetchall()
    # choose random 10 from all these
    random.shuffle(result)
    return {"questions":json.dumps(result[:10])}

@app.route('/postprofile/<name>/<rollno>/<phone_no>/<referal>/<imageurl>')
def postprofile(name,rollno,phone_no,referal,imageurl):
    referal=base64.b64decode(referal)
    imageurl=base64.b64decode(imageurl)
    imageurl=(imageurl).decode('utf-8')
    referal=(referal).decode('utf-8')
    # print((imageurl).decode('utf-8')) 
    print(imageurl)
    print(referal)
    try:
        # print("INSERT into profile VALUES('"+rollno+"',"+str(phone_no)+",'"+name+"','"+str(imageurl)+"','"+referal+"')")
        query = cursor.execute("INSERT into profile VALUES('"+rollno+"',"+str(phone_no)+",'"+name+"','"+imageurl+"','"+referal+"')")
        # print(query)
        connection.commit()
        return {'status': 'success'}

    except:
        # print("UPDATE profile set name = '"+name+"',phone = "+str(phone_no)+",image_url = '"+imageurl+"' where id='"+rollno+"'");
        query = cursor.execute("UPDATE profile set name = '"+name+"',phone = "+str(phone_no)+",image_url = '"+str(imageurl)+"' where id='"+rollno+"'")
        print(query)
        connection.commit()
        return {'status': 'success'}


    else:
        #print("INSERT INTO score VALUES(NULL, '"+rollno+"',10,"+str(1537940897)+",1),(NULL, '"+referal+"',10,"+str(1537940897)+",1)")
        #query = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"',10,"+str(1537940897)+",1),(NULL, '"+referal+"',10,"+str(1537940897)+",1)")
        query = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"',10,"+str(time.time()+(3600*24*30*6))+",1),(NULL, '"+referal+"',10,"+str(time.time()+(3600*24*30*6))+",1)")
        #query = cursor.execute("INSERT into profile VALUES('"+rollno+"',"+str(phone_no)+",'"+name+"',NULL, NULL)")
    return {'status': 'success'}

@app.route('/checkuser/<phone_no>')
def checkuser(phone_no):
    query = cursor.execute("SELECT COUNT(*) as user_count from profile where phone="+phone_no)
    result = cursor.fetchone()
    print(result['user_count'])
    if result['user_count'] > 0:
        query = cursor.execute("SELECT * from profile where phone="+phone_no)
        result = {'exists': True, 'data': cursor.fetchone()}
        return result
    else:
        return {'exists': False, 'data': {}}


@app.route('/getprofile/<user_id>')
def getprofile(user_id):
    #print("SELECT profile.name as name, profile.id as rollno, profile.image_url as profile_pic, (SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) as score FROM profile WHERE profile.id ='"+user_id+"'")
    query = cursor.execute("SELECT profile.name as name, profile.id as rollno, profile.image_url as profile_pic, (SELECT SUM(referal_score) FROM score WHERE score.profile_id=rollno) as score FROM profile WHERE profile.id ='"+user_id+"'")
    result = cursor.fetchall()
    # print(result1)
    return result

@app.route('/deletewallpost/<int:image_id>')
def deletewallpost(image_id):
    query = cursor.execute("DELETE from wall where wall.id='"+str(image_id)+"'")
    if query:
        return {'status': 'success'}
    else:
        return {'status': 'fail'}

@app.route('/postgamestatus/<user_id>')
def postgamestatus(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',0,0,0)")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}

@app.route('/gettambolastatus/<user_id>')
def gettambolastatus(user_id):
    query = cursor.execute("SELECT FORMAT(SUM(tambola_status),0) as tambolastatus from game_status where user_id='"+user_id+"'")
    result = cursor.fetchone()
    return result

@app.route('/posttambolastatus/<user_id>')
def posttambolastatus(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',0,1,0)")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}

@app.route('/getquizstatus/<user_id>')
def getquizstatus(user_id):
    query = cursor.execute("SELECT FORMAT(SUM(quiz_status),0) as quizstatus from game_status where user_id='"+user_id+"'")
    # print("SELECT FORMAT(SUM(quiz_status),0) as quizstatus from game_status where user_id='"+user_id+"'")
    result = cursor.fetchone()
    return result

@app.route('/postquizstatus/<user_id>')
def postquizstatus(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',1,0,0)")
    if query:
        return {'status':'success'}
    else:
        return {'status':'failure'}

@app.route('/getroulettecount/<user_id>')
def getroulettecount(user_id):
    query = cursor.execute("SELECT FORMAT(SUM(roulette_status),0) as roulettecount from game_status where user_id='"+user_id+"'")
    result = cursor.fetchone()
    return result

@app.route('/postroulettecount/<user_id>')
def postroulettecount(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',0,0,1)")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
