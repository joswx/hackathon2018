'''
This script is used to preprocess the news data in json format and output in csv format
'''

import pandas as pd
from afinn import Afinn

OUTPUT_DIRECTORY = "./news/"

if __name__ == "__main__":
	'''Load, preprocess, model and output in csv format'''
	df = pd.read_csv("./news/data.csv")
	df['publishedAt'] = df['publishedAt'].map(lambda x: x.replace("Z"," "))
	df['publishedAt'] = df['publishedAt'].map(lambda x: x.replace("T"," "))
	df['publishedAt'] = pd.to_datetime(df['publishedAt'],format='%Y-%m-%d %H:%M:%S')
	afinn = Afinn()
	scores = []
	for content in df['description']:
		try:
        	scores.append(afinn.score(content))
    	except:
        	scores.append(0)
	df['sentiment_score'] = pd.Series(scores).values
	df.to_csv(path.join(OUTPUT_DIRECTORY,'output.csv'))