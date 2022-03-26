## Import Dependencies

import tweepy 
import configparser # alternatives: json, yaml, toml, also environment variables

import pandas as pd
import re
import matplotlib.pyplot as plt
import plotly.express as px

from textblob import TextBlob


import datetime as dt
from dash import Dash, dcc, html, Input, Output

## Import Secrets

def get_api_client():
    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini') #read the config file


    #extract the information that you require
    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    ## Authenticate

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def get_latest_tweets(api):
    # api  = get_api_client()
    public_tweets = api.home_timeline()

    #Extract 100 tweets from the twitter user
    posts = api.user_timeline(screen_name = 'FabrizioRomano', count=10, lang ='en', tweet_mode='extended')


    ## Dataframe

    columns = ['TimeStamp', 'Users','Tweets']
    data = []
    for tweet in posts:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

    df = pd.DataFrame(data, columns=columns)
    return df 

def preprocess_tweets(df):
    # get_latest_tweets()
    #Change data time 
    df['Day'] = df["TimeStamp"].dt.strftime("%m/%d/%y")
    df['Time'] = df['TimeStamp'].dt.strftime("%H:%M")

    #Add the lenth of the tweet
    df['Text Length'] = df.Tweets.str.split().str.len()

    # Subjectivity tells you how opinionated a text is
    # Create two new coloums with sensitivity and polarity 
    df['Subjectivity'] = df['Tweets'].apply(getsubjectivity)
    df['Polarity'] = df['Tweets'].apply(getpolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    df['Tweets'] = df['Tweets'].apply(cleanText) #Apply function to the tweets 

    return df

def cleanText(text): 
    text = re.sub( r'@[A-Za-z0-9]+', '', text) 
    #sub will subsitute like @, + is added for one or more, r tells python the expression is a string, 'empty string'
    text = re.sub(r'#', '', text) #removes the hash tag symbol
    text = re.sub(r'RT[/s]', '', text) #Removes the retweets followed by one or more white spaces
    text = re.sub(r'https?:\/\/S+', '', text ) #Removes url, ? might have 0 or 1, S is it followed by one or more white spaces
    text = re.sub(r'\d+', '', text)
    return text

def getsubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getpolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score <0:
        return 'Negative'
    elif score == 0:
        return 'Netural'
    else:
        return 'Positive'
       
def download_file(tweets):
    tweets.to_csv('processed_df.csv')
    print('Saved File') # You  can log that the file has finished by printing saved file


api = get_api_client()
tweets = get_latest_tweets(api)
proccesed = preprocess_tweets(tweets)
download_file(proccesed) #Dont need a print as this the last step



