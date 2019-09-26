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

@app.route('/postgamestatus/<user_id>')
def postgamestatus(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',0,0,0)")
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


@app.route('/getleaderboard')
# Sample Response: [{"id": "17mi561", "name": "Daniyaal Khan", "score": 60.0}, {"id": "17mi560", "name": "Check", "score": 10.0}]
def getleaderboard():
    #print("SELECT p.id, p.name, p.image_url, ((SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=(UNIX_timestamp(timestamp(current_date))+19800)+(SELECT SUM(referal_score) FROM score WHERE profile_id=p.id)) as score FROM profile AS p ORDER BY score DESC LIMIT "+str(startfrom)+", "+str(startfrom+10))
    query = cursor.execute("SELECT p.id, p.name, p.image_url, ((SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=(UNIX_timestamp(timestamp(current_date))+19800) AND referal_score=0)) as score FROM profile AS p ORDER BY score DESC")
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

@app.route('/getwall/<int:start>/<user_id>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "s": 2}]
def getwall(start,user_id):
    query = cursor.execute("SELECT w.id as id, p.name as name, p.id as rollno, (SELECT COUNT(*) FROM likes WHERE post_id=w.id) AS likes, (Select count(*) from likes where post_id=w.id AND profile_id='"+user_id+"') as liked, w.image_url, p.image_url AS profile_pic  FROM wall as w, profile as p WHERE p.id=w.profile_id ORDER BY w.time DESC")
    result = cursor.fetchall()
    return json.dumps(result)



