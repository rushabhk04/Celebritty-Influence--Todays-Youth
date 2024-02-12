from pymongo import MongoClient
from datetime import datetime
import pytz
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np  
import time


def handle_mongodb_connection(func):
    def wrapper(*args, **kwargs):
        client = MongoClient('mongodb://localhost:27017/')
        db = client["team_caffeine"]
        try:
            return func(client, db, *args, **kwargs)
        finally:
            client.close()
    return wrapper



@handle_mongodb_connection
def get_like_counts_youtube(client, db, celeb_name):
    collection = db['youtube_data']
    video_records = collection.find()
    temp_count = 0
    video_count = 0
    for record in video_records:
        temp = record['video_info']['statistics']
        if record['Name'] == celeb_name:
            video_count += 1
            if temp.get('likeCount') is not None:
                temp_count += int(temp['likeCount'])
        
    return {
        celeb_name: temp_count
        }


@handle_mongodb_connection
def get_like_counts_reddit(client,db,subreddit):
    collection = db['reddit_data']
    post_record = collection.find()
    count_list = []
    temp_count = 0
    post_count = 0
    for post in post_record:
        if post['subreddit'] == subreddit:
            temp_count += int(post['ups'])
            post_count += 1

    return {
        subreddit: temp_count
    }




def start_influence():
    celeb_name = [
    "Cristiano Ronaldo",
    "Lionel Messi",
    "Selena Gomez",
    "Kylie Jenner",
    "Dwayne Johnson",
    "Ariana Grande",
    "Kim Kardashian",
    "Beyoncé",
    "Khloé Kardashian",
    "Kendall Jenner"
    ]

    celebrities = [
    "cristianoronaldo",
    "messi",
    "SelenaGomez",
    "KylieJenner",
    "DwayneJohnson",
    "ArianaGrande",
    "KimKardashianPics",
    "beyonce",
    "KhloeKardash",
    "kendalljenner"
    ]

    youtube_like_count = []
    for celeb in celeb_name:
        youtube_like_count.append(get_like_counts_youtube(celeb))
    print(youtube_like_count)
    
    reddit_count = []
    for subreddit in celebrities:
        reddit_count.append(get_like_counts_reddit(subreddit))
    plot_data(youtube_like_count, 'youtube')
    plot_data(reddit_count,'reddit')

def plot_data(data, source):
    keys = []
    values = [] 
    for item in data:
        key = list(item.keys())[0]
        value = list(item.values())[0]
        keys.append(key)
        values.append(value)

   
    plt.figure(figsize=(15, 10))
    plt.bar(keys, values, color='skyblue')
    plt.xticks(rotation=45, ha='right') 
    plt.xlabel('Celebrities')
    plt.ylabel('Likes')
    plt.title(f'Engagement Data Analysis {source}')
    t = time.time()
    plt.savefig(f'plots/influencePlots/plot_{source}_{time.ctime(t)}.png')
    plt.show()



 
if __name__ == "__main__":
    start_influence()