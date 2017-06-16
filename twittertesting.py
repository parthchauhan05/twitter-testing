import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import time
from math import inf

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'dDMSTUdejP0imRhb5Ip72NO4d'
		consumer_secret = '0l3HqzF6aqUGSljjun0YEgdF0Fqqnfq9gKglTmY0VfxCUsz9p1'
		access_token = '593620516-1VBe8ANxXHbD04mJNtE16oHGZ6dz1HwRiggGhKe7'
		access_token_secret = 'XpIjg3nZ7iDROF1rI2fI9w97PiRDj2rqKa6GeHxOHDbZI'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	t = time.time()
	api = TwitterClient()
	t1 = input("Enter 1st query:")
	t2 = input("Enter 2nd query:")
	# calling function to get tweets
	tweets1 = api.get_tweets(query = t1,count = 2**1000)
	tweets2 = api.get_tweets(query = t2,count = 2**1000)
	# print(tweets1[:10])
	# picking positive tweets from tweets
	try:
		ptweets1 = [tweet for tweet in tweets1 if tweet['sentiment'] == 'positive']
		# percentage of positive tweets
		print("Positive tweets percentage: {} %".format(100*len(ptweets1)/len(tweets1)))
		# picking negative tweets from tweets
		ntweets1 = [tweet for tweet in tweets1 if tweet['sentiment'] == 'negative']
		# percentage of negative tweets
		print("Negative tweets percentage: {} %".format(100*len(ntweets1)/len(tweets1)))
		# percentage of neutral tweets
		print("Neutral tweets percentage: {} % ".format(100*(len(tweets1) - len(ntweets1) - len(ptweets1))/len(tweets1)))
	except ZeroDivisionError:
		print("Poor Twitter Performance, "+t1)

	try:
		ptweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'positive']
		# percentage of positive tweets
		print("Positive tweets percentage: {} %".format(100*len(ptweets2)/len(tweets2)))
		# picking negative tweets from tweets
		ntweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'negative']
		# percentage of negative tweets
		print("Negative tweets percentage: {} %".format(100*len(ntweets2)/len(tweets2)))
		# percentage of neutral tweets
		print("Neutral tweets percentage: {} % ".format(100*(len(tweets2) - len(ntweets2) - len(ptweets2))/len(tweets2)))
	except ZeroDivisionError:
		print("Poor Twitter Performance, "+t2)

	try:
		if (100*len(ptweets1)/len(tweets1)) > (100*len(ptweets2)/len(tweets2)):
			print(t1+' Wins')
		elif (100*len(ptweets1)/len(tweets1)) < (100*len(ptweets2)/len(tweets2)):
			print(t2+' Wins')
		else:
			print("Both are Equal")
	except ZeroDivisionError:
		pass
		
	print("Time : {} seconds".format(time.time()-t))
	# printing first 5 positive tweets
	# print("\n\nPositive tweets:")
	# for tweet in ptweets[:10]:
	# 	print(tweet['text'])

	# # printing first 5 negative tweets
	# print("\n\nNegative tweets:")
	# for tweet in ntweets[:10]:
	# 	print(tweet['text'])

if __name__ == "__main__":
	# calling main function
	main()
