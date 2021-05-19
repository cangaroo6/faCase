from flask import Flask, request, render_template
import requests as req
import pandas as pd
import sys

# initialize flask app
app = Flask(__name__)

# scrape the 5 highest scored posts from a reddit URL
def scrapeTop5Posts(text):
	# process different types of URL notation
	if text[0:12] == 'https://www.': url = text + '/.json'
	elif text[0:4] == 'www.': url = 'https://' + text + '/.json'
	else: url = 'https://www.' + text + '/.json'
	# try to access URL information and process them into a top 5 list
	try:
		response = req.request(method='GET', url=url, headers={'User-agent': 'RedditScraper'})
		# transfer json result to dataframe to simplify further processing
		df = pd.DataFrame()
		for post in response.json()['data']['children']:
			df = df.append({
				'title': post['data']['title'],
				'score': post['data']['score']
			}, ignore_index=True)
		top5 = df.sort_values('score', ascending=False).head()
		return top5['title'].tolist()
	# handle different errors resulting from an invalid URL request
	except:
		if 'reddit' not in url: return 'Your URL does not refer to a reddit page.'
		# URL not accessible or returned json structure not proccesible
		elif not response.ok or sys.exc_info()[0] == TypeError: return 'Your reddit URL does not refer to a reddit or subreddit.'
		else: return 'Your URL request is not valid. Please try another one.'

# display/initialize html template
@app.route('/')
def home():
	return render_template('redditSubmit.html')

# process a URL when submitted
@app.route('/', methods=['POST'])
def processURLSubmit():
	text = request.form['redditURL']
	result = scrapeTop5Posts(text)
	if text == '': return render_template('redditSubmit.html', error='Please enter a reddit URL.')
	else:
		if isinstance(result, list): return render_template('redditSubmit.html', posts=result)
		else: return render_template('redditSubmit.html', error=result)

# enable debug mode
if __name__ == '__main__':
	app.run(debug=True)