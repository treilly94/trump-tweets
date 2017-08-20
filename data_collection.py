import requests
import pandas as pd
from bs4 import BeautifulSoup


def sentence_reader():
    """

    :rtype: object
    """
    # Get Html and create Soup
    r = requests.get('https://twitter.com/realDonaldTrump?lang=en-gb')
    soup = BeautifulSoup(r.content, "lxml")

    # Read data into dataframe
    df = pd.DataFrame({"Time": [], "Text": []})
    for tweet in soup.find_all("div", {"class": "tweet"}):
        # Get the time of the tweet
        time = tweet.find("a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})['title']
        # Get text of tweet
        text = tweet.find("div", {"class": "js-tweet-text-container"}).get_text().strip()
        # Add to df
        temp_df = pd.DataFrame({"Time": time, "Text": [text]})
        df = df.append(temp_df)

    # Repair the df index
    df.reset_index(drop=True, inplace=True)

    # Convert string to timestamp
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p - %d %b %Y', errors='ignore')

    return df


def word_splitter(df):
    # Split the sentences into individual words
    words_df = pd.concat([pd.Series(row['Time'], row['Text'].split(' ')) for _, row in df.iterrows()]).reset_index()
    words_df.columns = ['Word', 'Time']
    # Make words more consistent
    words_df['Word'] = words_df['Word'].str.strip('.')
    words_df['Word'] = words_df['Word'].str.strip(',')
    words_df['Word'] = words_df['Word'].str.lower()

    return words_df
