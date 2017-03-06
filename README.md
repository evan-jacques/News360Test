# News360Test
Your service should :

1.    launch every 10 minutes and download all new tweets (or use Twitter streams, but it’s more complicated)
	- twitter_search.py does this

2.    store tweet texts and attributes into storage
	- twitter_search,py does this

3.    group tweets about the same event into one cluster
	- clustering.py does this. I used cosine comparison to compare the different tweets. I did not write the code for that, I found it here: http://stackoverflow.com/questions/15173225/how-to-calculate-cosine-similarity-given-2-sentence-strings-python. It checks compared to all the tweets gathered which works fine since I didn't collect much data to test it on however it should probably be limited to looking only at the past few hours or so to speed it up.

4.    recognize events that are hot, urgent and worthy to send notification to users (not more than 2 per day)
	- simply found clusters of tweets that were larger than 4. I figured important stories would be covered by many of the news outlets so I figured that that was the easiest way to determin if something was significant. 4 is just an arbitrary number I picked based on the data I collected to test this. In the cluster file outputed the important clusters are marked with ****IMPORTANT****.

5.    select the “best” tweet from every such cluster
	- best tweet in the file is the first one of the group. All other tweets in the cluster are below in indented.

6.    create file with results: (tweet URL, tweet text, tweet date and any additional information you found useful) for every such cluster
	- file created in clustering.py

