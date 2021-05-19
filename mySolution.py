from flask import Flask, request, render_template
import requests as req
import pandas as pd


app = Flask(__name__)

def scrapeTop5Posts(text):
	url = 'https://www.' + text + '/.json'
	try:
		response = req.request(method='GET', url=url, headers={'User-agent': 'RedditScraper'})
		df = pd.DataFrame()
		for post in response.json()['data']['children']:
			df = df.append({
				'title': post['data']['title'],
				'score': post['data']['score']
			}, ignore_index=True)
		top5 = df.sort_values('score', ascending=False).head()
		return top5['title'].tolist()
	except:
		return None

@app.route('/')
def home():
	return render_template('redditSubmit.html')

@app.route('/', methods=['POST'])
def processURLSubmit():
	text = request.form['redditURL']
	posts = scrapeTop5Posts(text)
	if posts is not None: return render_template('redditSubmit.html', posts=posts)
	else: return render_template('redditSubmit.html', error='Your URL request is not valid. Please try another one.')


if __name__ == '__main__':
	app.run(debug=True)