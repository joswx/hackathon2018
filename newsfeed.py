
'''
This script is dedicated to crawl the Reuters newsfeed data through newsfeed api.
The query can be customized its keywords, sources, language, and number of news.
News are requested and stored in csv format on local machine/push to mongodb.
'''

KEY = "486f092b62a44d74a17e6c733de7f283"
OUTPUT_DIRECTORY = "./news/"

from newsapi import NewsApiClient
import json
import os
from os import path
import csv


'''A newsfeed object that can connect to newsapi and customize its query.

Attributes:
	q: keyword for the query, default = Empty string
	category: default = 'business'
	language: default = 'en'
	page: number of news requested, default = 0'''
class NewsfeedGetter(object):

	def __init__(self,q='business',sources = 'reuters', language='en',page=50):
		self.q = q
		self.sources = sources
		self.language = language
		self.page = page
		print("_______Object Initilazed_________")

	'''Mutatiors'''
	def __set_q(self,keyword):
		self.q = keyword
	def __set_sources(self,sources):
		self.sources= sources
	def __set_language(self,language):
		self.language = language
	def __set_page(self,page):
		self.page = page

	'''Attributes Printout'''
	def toString(self):
		print("q: %s, sources: %s,language: %s, page: %s" % (self.q, self.sources, self.language,self.page))
	'''Writer method'''
	def writer(self):
		newsapi = NewsApiClient(api_key = KEY)
		collection = []
		try:
			for i in range(1,self.page):
				top_headlines = newsapi.get_everything(
											sources = self.sources,
											language = self.language,
											page = i )
				for article in top_headlines['articles']:
					collection.append(article)
			keys = collection[0].keys()
			with open(path.join(OUTPUT_DIRECTORY,'data.csv'),'w',encoding ='utf-8') as f:
				dict_writer = csv.DictWriter(f,keys)
				dict_writer.writeheader()
				dict_writer.writerows(collection)
		except:
			raise Exception("Unable to retrieve the latest feed.")

def __handle_output_directory(output_directory):
	if not path.isdir(output_directory):
		try:
			os.makedirs(output_directory)
		except os.error:
			raise Exception("Error creating output_directory: {}".format(
				output_directory))

if __name__ == "__main__":
	nf = NewsfeedGetter()
	nf.writer()


