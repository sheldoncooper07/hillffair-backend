from flask import Flask, request
from functools import wraps
import json, time
from datetime import datetime
import random
import pymysql.cursors
import base64
app = Flask(__name__)
import faceSmash as faceSmash

global cursor





connection = pymysql.connect(host='sql12.freesqldatabase.com',
                                       # port=3306,
                                         user='sql12306111',
                                         password='CABFDtx5cP',
                                         db='sql12306111',
                                         cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()




app.add_url_rule('/facesmash', 'faceSmash.faceSmash', faceSmash, methods=['GET', 'POST'])



@app.route('/makeuser' , methods=['GET'])
def hello():
        query = "INSERT into profile VALUES ('abcd',18155,'CSE',8580635669,'DEF',12,1,'google.com')"
        cursor.execute(query)
        connection.commit()
        print("Done")
        return "hello"
@app.route('/makeclub',methods=['GET'])
def makeclubs():
    query = "INSERT into clubs VALUES (123,'App Team','google.com','Hiii')"
    cursor.execute(query)
    connection.commit()
    return "done"
        
        



@app.route('/postwall/<rollno>/<imageurl>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "likes": 2}]
def postwall(rollno,imageurl):

    imageurl=imageurl
    #print("INSERT into wall values(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    query = cursor.execute("INSERT into Wall values(NULL,'"+rollno+"','"+imageurl+"', "+str(int(time.time()+19800))+")")
    cursor.execute(query);
    connection.commit();
    return {'status': 'success'}



@app.route('/user',methods=['POST'])
def user():
    rollno,branch,mobile,referal_friend,name,gender,image_url=request.form.rollno,request.form.branch,request.form.mobile,request.form.referal_friend,request.form.name,request.form.gender,request.form.image_url
    query=query = cursor.execute("INSERT into profile values('"+rollno+"','"+branch+"','"+mobile+"','"+referal_friend+"',+name,gender,image_url")
    connection.commit()
    return {'status':'success'}
    
 #tested
@app.route('/user/<firebase_id>',methods=['GET'])
def fid(firebase_id):
     query="SELECT * FROM profile AS user HAVING firebase_id='"+firebase_id+"'"
     cursor.execute(query)
     user=cursor.fetchall()
     #connection.commit()
     print(user)
     return user
    
@app.route('/like',methods=['POST'])#FIX THIS
def like():
    firebase_id=request.form.firebase_id
    image_url=request.form.image_url
    query="UPDATE wall SET likes=likes+1 WHERE firebase_id='"+firebase_id+"'"
    cursor.execute(query)
    connection.commit()
    return {status_code:200}
    
   
@app.route('/faceSmash',methods=['POST'])
def faceSmashP():
    image_url=request.form.image_url
    firebase_id=request.form.firebase_id #user or firebase id??? todo
    #todo


@app.route('/quiz/questions',methods=['POST'])
def quiz():
    category=request.form.category
    query="SELECT * FROM quiz AS ques WHERE category='"+category+"'"
    cursor.execute(query)
    questions=connection.fetchall();
    return questions
    #random on client side
    
    
#@app.route('/profile',methods=['POST'])
#def profile():
#    firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url=request.forms.firebase_id,request.form.rollno,request.form.branch,request.form.mobile,request.form.referl_friend,request.form.name,request.form.gender,request.form.image_url
#    query="INSERT INTO profile VALUES(firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url"
#    cursor.execute(query)
#    connection.commit()
#    return {status_code:200}
   
#@app.route('/profile',methods=['GET'])
#def profile():
#   firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url=request.forms.firebase_id,request.form.rollno,request.form.branch,request.form.mobile,request.form.referl_friend,request.form.name,request.form.gender,request.form.image_url
#   query=" profile VALUES(firebase_id,rollno,branch,mobile,referal_friend,name,gender,image_url"
#    cursor.execute(query)
#    connection.commit()
#   return {status_code:200}   



@app.route('/club_info/<club_name>' ,methods=['GET'])
def club():
    query="SELECT * from club AS details where name='"+club_name>+"'"
    cursor.execute(query)
    details=connection.fetchone()
    return {details}
    
@app.route('/core_team/<core_name>' ,methods=['GET'])  
def core():
    query="SELECT * from coreteamcas core_detail where name='"+core_name+"'"
    cursor.execute(query)
    core_details=connection.fetchone()
    return {core_detail}
    
    
    
    
@app.route('/sponsors')
def sponsors():
    query="SELECT * from sponsors as sponsor"
    cursor.execute(query)
    sponsor=connection.fetchall()
    return {sponsor}
    
@app.route('/leaderboard')
def leaderboard():
    query="SELECT name,points as details from profile "
    cursor.execute(query)
    details=connection.fetchall()
    return {details}
    
    
@app.route('/rewards',methods=['POST'])
def rewards():
    firebase_id=request.form.firebase_id
    candies=request.form.sub_candies
    query="UPDATE profile SET points=points-'"+candies+"' WHERE firebase_id='"+firebase_id+"'"
    
    
    #---------------------------------------------------------------------------
    

@app.route('/getwall/<int:start>/<user_id>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "likes": 2}]
def getwall(start,user_id):
    query = cursor.execute("SELECT w.id as id, p.name as name, p.id as rollno, (SELECT COUNT(*) FROM likes WHERE post_id=w.id) AS likes, (Select count(*) from likes where post_id=w.id AND profile_id='"+user_id+"') as liked, w.image_url, p.image_url AS profile_pic  FROM wall as w, profile as p WHERE p.id=w.profile_id ORDER BY w.time DESC")
    result = cursor.fetchall()
    return result





@app.route('/getschedule')
def getschedule():
    query = cursor.execute("SELECT name as club_name, event_id,event_name,event_time,club_logo FROM events,clubs WHERE events.club_id=clubs.id")
    result = cursor.fetchall()
    #for x in result:
        #x["event_time"] = x["event_time"].timestamp()
    return result

@app.route('/posteventlike/<user_id>/<event_id>')
def posteventlike(user_id, event_id):
    userCheck = cursor.execute("SELECT * from profile where id = %s", (user_id))
    if userCheck == 0:
        return {'status': 'No such user'}
    eventCheck = cursor.execute("SELECT * from events where event_id = %s", (event_id))
    if eventCheck == 0:
        return {'status': 'No such event'}
    query = cursor.execute("SELECT * from event_likes where user_id = %s AND event_id = %s", (user_id, event_id))
    if query == 0:
        cursor.execute("INSERT INTO event_likes VALUES (NULL, %s, %s)", (event_id, user_id))
        return {'status': 'success'}
    else:
        return {'status': 'Already Liked'}

@app.route('/geteventlike/<event_id>')
def geteventlike(event_id):
    query = cursor.execute("SELECT COUNT(*) from event_likes where event_id = %s", event_id)
    result = cursor.fetchone()
    return {'likes': result["COUNT(*)"]}






winarray = list(range(1,91))
random.shuffle(winarray)

@app.route('/gettambolanumber')
def gettambolanumber():
    time = int(datetime(2018, datetime.now().month, datetime.now().day, 22, 0).timestamp())
    current = int(datetime.now().timestamp())
    if(0 <= current - time <= 3600):
        i = ((current - time) // 15) % 90
        return {'number' : winarray[i]}
    else:
        return {'status': 'Unavailable'}

@app.route('/posttambolaresult')
def posttambolaresult():
    return 'Hello, World!'

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
    return {'questions':result[:10]}

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
    except:
        # print("UPDATE profile set name = '"+name+"',phone = "+str(phone_no)+",image_url = '"+imageurl+"' where id='"+rollno+"'");
        query = cursor.execute("UPDATE profile set name = '"+name+"',phone = "+str(phone_no)+",image_url = '"+str(imageurl)+"' where id='"+rollno+"'")
        print(query)

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
    query = cursor.execute("SELECT FORMAT(SUM(roulette_status),0) as roulettecount from game_status where user_id='"+user_idx+"'")
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
