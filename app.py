from flask import Flask, render_template, request
from stream_tweets import twitter
import pickle
import os
from fasttextmodel import preprocessor, predict

app = Flask(__name__)
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                                    'speechclassifier/pkl_objects', 'classifier.pkl'),
                                    'rb'))


@app.route('/')
def stream_tweets():
    # Call the get_stream function to fetch tweets
    tweets = twitter.get_stream()
    processed_tweets = []
    for tweet in tweets:
        processed_tweets.append(preprocessor(tweet['text']))
        #clf.predict(preprocessor(tweet['text']))[0]

    # Pass the tweets data to the template
    return render_template('tweets.html', tweets=tweets)

@app.route('/vote', methods=['POST'])
def vote():
    # Get the tweet ID and vote value from the form
    tweet_id = request.form['tweet_id']
    vote = request.form['vote']


if __name__ == '__main__':
    app.run(port=8000)

