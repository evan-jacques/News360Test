import cosine_comparison, unicodedata, re, database

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

def findIdInCluster(id, cluster):
	for x in range(0,len(cluster)):
		if id in cluster[x]:
			return x
	return -1

def tweetToVector(tweet):
	twString = unicodedata.normalize('NFKD', tweet[0]).encode('ascii','ignore')
	twText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', twString)
	vec = cosine_comparison.text_to_vector(twText)
	return vec

def groupSimilarClusters(clusterIds):
	tweets = database.getAllTweetsById()
	for id in tweets:
		similarClusters = []
		for x in range(0,len(clusterIds)):
			if id in clusterIds[x]:
				similarClusters.append(x)
		if len(similarClusters) > 1:
			for y in range(1,len(similarClusters)):
				for id2 in clusterIds[similarClusters[y]]:
					if id2 in clusterIds[similarClusters[0]]:
						continue
					clusterIds[similarClusters[0]].append(id2)
			deletedCount = 0
			for z in range(1,len(similarClusters)):
				del clusterIds[similarClusters[z] - deletedCount]
				deletedCount += 1

	return clusterIds		

def clusterTweets():
	tw = database.getAllTweetsBySource()
	seenSources = []
	clusterIds = []

	for source in newsSources:
		seenSources.append(source)
		for tweet in tw[source]:
			deleteCluster = True
			idLocation = findIdInCluster(tweet[1],clusterIds)
			if idLocation == -1:
				clusterIds.append([tweet[1]])
				idLocation = len(clusterIds) - 1
			vec1 = tweetToVector(tweet)
			for s in newsSources:
				if s in seenSources:
					continue
				for t in tw[s]:
					idLoc = findIdInCluster(t[1],clusterIds)
					if idLoc == idLocation:
						continue
					vec2 = tweetToVector(t)
					cosine = cosine_comparison.get_cosine(vec1, vec2)
					if cosine > 0.55:
						deleteCluster = False
						clusterIds[idLocation].append(t[1])

			if deleteCluster:
				del clusterIds[len(clusterIds) - 1]

	clusterIds = groupSimilarClusters(clusterIds)
	return clusterIds

def writeClustersToFile():
	tweets = database.getAllTweetsById()
	clusters = clusterTweets()
	clusters_file = open('clusters.txt', "w")
	for cluster in clusters:
		bestId = 0
		bestCount = 0
		for id in cluster:
			favs_count = int(unicodedata.normalize('NFKD', tweets[id][2]).encode('ascii','ignore'))
			if favs_count > bestCount:
				bestId = id
				bestCount = int(tweets[id][2])
		if len(cluster) > 4:
			clusters_file.write( "****IMPORTANT****\n")

		clusters_file.write(	unicodedata.normalize('NFKD', tweets[bestId][0]).encode('ascii','ignore') + "\n" 
				      + "https://twitter.com/" + tweets[bestId][5] + "/status/" + unicodedata.normalize('NFKD', tweets[bestId][1]).encode('ascii','ignore') + "\n" 
				      + unicodedata.normalize('NFKD', tweets[bestId][2]).encode('ascii','ignore') + "\n" 
				      + unicodedata.normalize('NFKD', tweets[bestId][4]).encode('ascii','ignore') + "\n\n" )
		for id in cluster:
			if id == bestId:
				continue
			clusters_file.write("\t" + unicodedata.normalize('NFKD', tweets[id][0]).encode('ascii','ignore') + "\n\t" 
						 + "https://twitter.com/" + tweets[id][5] + "/status/" + unicodedata.normalize('NFKD', tweets[id][1]).encode('ascii','ignore') + "\n\t" 
						 + unicodedata.normalize('NFKD', tweets[id][2]).encode('ascii','ignore') + "\n\t" 
						 + unicodedata.normalize('NFKD', tweets[id][4]).encode('ascii','ignore') + "\n\n" )
	clusters_file.close()
	
writeClustersToFile()
