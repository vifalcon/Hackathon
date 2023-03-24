import csv, time
from pathlib import Path
import requests, json
import config

# curl -X POST 'https://api.twitter.com/2/tweets/search/stream/rules' \
# -H "Content-type: application/json" \
# -H "Authorization: Bearer $APP_ACCESS_TOKEN" -d \
# '{
#   "add": [
#     {"value": "cat has:images", "tag": "cats with images"}
#   ]
# }'

#{'value': "(bitcoin mining) -forex -earn -is:retweet  lang:en", "tag": "bitcoin-mining tweets"},

class twitter:

  global headers

  headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer" + " " + str(config.token)

    }

  @staticmethod
  def set_rules():
  # the value is what we are searching for, so any tweet with the word 'cat'
    # cat is the variable, has:images is a condition, the : is a boolean operator
  # the tag allows us to identify which tweet matches which rule when it comes through the stream
    # this is if we have many values


    rules = [
       {'value': 'faggot lang:en', 'tag': 'lgbtq'},
       {'value': 'i hate you -is:retweet lang:en', 'tag': 'lgbtq'},
       {'value': 'shutup fag lang:en', 'tag': 'lgbtq'},
       {'value': 'kill yourself -is:retweet lang:en', 'tag': 'lgbtq'},
       {'value': 'shutup pussy  lang:en', 'tag': 'offensive'},
       {'value': 'shutup bitch lang:en', 'tag': 'offensive'},
       {'value': 'fuck you -is:retweet lang:en', 'tag': 'offensive'}
       #cleanenery hashtag
    ]

    json_payload = {
    'add': rules
    }

    r = requests.request("POST", config.twitter_url, headers=headers, json=json_payload)

    if r.status_code != 201:
          raise Exception(
            "Cannot add the rules (http error {}): {}".format(r.status_code, r.text)
          )
    print(json.dumps(r.json()))

  @staticmethod
  def get_rules():
    r  = requests.request('GET', config.twitter_url, headers=headers)

    if r.status_code != 200:
        raise Exception (
            "Cannot get the rules (http error {}): {}".format(r.status_code, r.text)
        )


    print(json.dumps(r.json()))
    #print(r.json())
    return r.json()


  @staticmethod
  def delete_rules(rules):
    if rules is None or "data" not in rules:
        return None


    print(rules)
    ids = list(map(lambda rule: rule["id"], rules["data"]))

    print(ids)
    payload = {'delete': {'ids': ids}}

    r  = requests.request('POST', config.twitter_url, headers=headers, json=payload)

    if r.status_code != 200:
        raise Exception (
          "Cannot delete the rules (http error {}): {}".format(r.status_code, r.text)
        )

    print(r.text)


  @staticmethod
  def get_stream():

    r = requests.request("GET", config.twitter_search, headers=headers, stream=True)

    if r.status_code != 200:
          raise Exception(
            "Cannot continue stream (http error {}): {}".format(r.status_code, r.text)
          )

    tweets = list()
    for line in r.iter_lines():
          if line:
            decoded_line = line.decode('utf-8')
            s = json.loads(decoded_line)
            data = s['data']
            tag = s['matching_rules'][0]['tag']
            tweet = data['text']
            print(tweet)
            tweets.append({'tag': tag, 'text': tweet})
            if len(tweets) > 8:
                return tweets
            




          #print(tweets)

    return tweets

              # print(data)
              # print(tweets)






twitter = twitter()

#twitter.set_rules()

#rules = twitter.get_rules()
# print(rules)

# twitter.delete_rules(rules)

#tweets = twitter.get_stream()
#print(len(tweets))

#twitter.tweets_to_csv(tweets)