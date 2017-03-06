import mysql.connector

newsSources = [ 'nytimes',
	      	'thesunnewspaper',
		'thetimes', 
		'ap', 
		'cnn', 
		'bbcnews', 
		'cnet', 
		'msnuk', 
		'telegraph', 
		'usatoday', 
		'wsj', 
		'washingtonpost', 
		'bostonglobe', 
		'newscomauhq', 
		'skynews', 
		'sfgate', 
		'ajenglish', 
		'independant', 
		'guardian', 
		'latimes', 
		'reutersagency', 
		'abc', 
		'bw', 
		'time' ]

def dbConnect():
	cnx = mysql.connector.connect(user='', password='', host='', database='')
	return cnx

def dbDisconnect( db_conn ):
	db_conn.close()

def getAllTweetsById():
	db_conn = dbConnect()
	tweets = dict()

	for source in newsSources:
		cursor = db_conn.cursor()
		get_tweets = ('SELECT text, id, favorite_count, entities, created_at FROM ' + source )
		cursor.execute( get_tweets )
		for (text, id, favorite_count, entities, created_at) in cursor:
			tweets[id] = (text, id, favorite_count, entities, created_at, source)
		cursor.close()

	dbDisconnect(db_conn)
	return tweets

def getAllTweetsBySource():
	db_conn = dbConnect()
	tw = dict()

	for source in newsSources:
		tw[source] = []
		cursor = db_conn.cursor()
		get_tweets = ('SELECT text, id, favorite_count, entities, created_at FROM ' + source )
		cursor.execute( get_tweets )
		for (text, id, favorite_count, entities, created_at) in cursor:
			tw[source].append((text, id, favorite_count, entities, created_at))
		cursor.close()

	dbDisconnect(db_conn)
	return tw
