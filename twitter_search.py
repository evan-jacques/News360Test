# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import time, database, mysql.connector

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

def twitterConnect():
	# Variables that contains the user credentials to access Twitter API 
	ACCESS_TOKEN = ''
	ACCESS_SECRET = ''
	CONSUMER_KEY = ''
	CONSUMER_SECRET = ''

	oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

	# Initiate the connection to Twitter Streaming API
	twitter_conn = Twitter(auth=oauth)
	return twitter_conn

def getTweets( db_conn, twitter_conn ):
	cursor = db_conn.cursor()

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

	for source in newsSources:
		tweets = twitter_conn.statuses.user_timeline(screen_name=source)
		for tweet in tweets:
			text = tweet['text']
			id = tweet['id']
			favorite_count = tweet['favorite_count']
			entities = json.dumps(tweet['entities'])
			created_at = tweet['created_at']

			add_tweet = ('INSERT INTO ' + source + ' (text, id, favorite_count, entities, created_at) VALUES ( %s, %s, %s, %s, %s )')
			tweet_data = (text, id, favorite_count, entities, created_at)
			try:
				cursor.execute( add_tweet, tweet_data )
			except mysql.connector.errors.IntegrityError:
				continue
		
	db_conn.commit()
	cursor.close()
		
def main():
	while(True):	
		print 'starting'
		dbConn = database.dbConnect()
		twConn = twitterConnect()
		getTweets( dbConn, twConn )
		database.dbDisconnect( dbConn )
		print 'sleeping'
		time.sleep(600)
	

if __name__ == "__main__": main()
