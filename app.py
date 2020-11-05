import pandas as pd
#import nltk
from wordcloud import WordCloud, STOPWORDS
import re
import emoji
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from textblob import TextBlob
import folium
from streamlit_folium import folium_static
import json
from geopy.geocoders import Nominatim



def give_emoji_free_text(text):
    try:
        return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))
    except:
        return emoji.get_emoji_regexp().sub(r'', text)

def make_wordcloud(tweets):
    tweets = tweets.apply(lambda x: re.sub(r"http\S+", "", str(x)))
    tweets = tweets.apply(lambda x: give_emoji_free_text(x))
    tweets = tweets.apply(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
    tweets = tweets.apply(lambda x: x.lower().split())
    tweets = tweets.apply(lambda x: [word for word in x if word not in STOPWORDS])
    words = " "
    for l in tweets.values:
        words = words + " ".join(l) + " "
    wordcloud = WordCloud(width=800, height=500,
                          background_color='black',
                          min_font_size=10).generate(words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()
    st.image(wordcloud.to_array())

def plot_sentiment(tweets):
    tweets = tweets.apply(lambda x: re.sub(r"http\S+", "", str(x)))
    tweets = tweets.apply(lambda x: give_emoji_free_text(x))
    sentiment_objects = [TextBlob(tweet) for tweet in tweets]
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
    bins = st.slider(min_value=10, max_value=30, step=1, label='Number of bins')
    fig = px.histogram(x=sentiment_df['polarity'], nbins=bins)
    st.plotly_chart(fig)

def make_map(arr):
    if len(arr)>0:
        mapD = folium.Map(location=[19.076090, 72.877426], zoom_start=10)
        geolocator = Nominatim(user_agent="http")
        for item in arr:
            i = json.loads(item.replace('\'', '\"'))
            coord = i['coordinates']
            str_coord = ""+str(coord[0])+", "+str(coord[1])
            location = geolocator.reverse(str_coord)
            folium.Marker(coord, popup=location).add_to(mapD)
        folium_static(mapD)
    else:
        st.text('No Geo data available')


df = pd.read_csv('dabbawala.csv')
#df_mum = pd.read_csv('.\BDE Dabbawala\dabbawala_mumbai.csv')
df['date'] = pd.to_datetime(df['date'])
df_mum['date'] = pd.to_datetime(df_mum['date'])


since = pd.to_datetime(st.sidebar.date_input('since: '))
until = pd.to_datetime(st.sidebar.date_input('Until: '))
mask = (df['date'] >= since) & (df['date'] <= until)
working_data = df.loc[mask]

df_date = working_data.groupby('date')['date'].size().to_frame()
df_date.columns = ['counts']
fig = px.line(df_date, x=df_date.index, y=df_date['counts'], title='Tweet counts')
st.plotly_chart(fig)
make_wordcloud(working_data['tweet'])
plot_sentiment(working_data['tweet'])
make_map(working_data[working_data['place'].notna()]['place'].unique())
