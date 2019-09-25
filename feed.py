@app.route('/feed',methods=['POST'])
def feed(firebase_id,imageurl):
	firebase_id=request.form.firebase_id
	url=request.form.image_url
	query="INSERT INTO wall VALUES(id,'"+firebase_id+"',0,'"+imageurl+"')"
	cursor.execute(query)
	connection.commit()
	return {status_code:200}
   




@app.route('/feed/<page_index>/<firebase_id>',methods=['GET'])
def feedg():
	query="SELECT * FROM wall as photos ORDER BY id LIMIT (page_index-1)*10+1,(page_index*10) DESC"
	ret_arr=[]
	cursor.execute(query)
	photos=cursor.fetchall()
	for i in range(0,photos.length()):
		cursor.execute("SELECT * FROM likes as like WHERE firebase_id='"+firebase_id+"' AND id='"+photos[i].id+"'") 
		like=cursor.fetchone()
		if(like):
			q="COUNT * FROM likes where post='"+photots[i].id+"'"
			cursor.execute(q)
			count=cursor.fetchall()
			ret_arr.append({"image_url":photos[i].url,"likes":count,"liked":1})
		else:
			q="COUNT * FROM likes where post='"+photots[i].id+"'"
			cursor.execute(q)
			count=cursor.fetchall()
			ret_arr.append({"image_url":photos[i].url,"likes":count,"liked":0})
