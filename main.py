import dbm
from reddit import new_reddit_fetch
from pymongo import MongoClient
from youtube import fetch_youtube_data
from reddit import politics_fetch_data
import time
import datetime
import logging
import pytz  #for time zone conversion


# Handling the MongoDB connection here
def handle_mongodb_connection(func):
    def wrapper(*args, **kwargs):
        client = MongoClient('mongodb://localhost:27017/')
        db = client["team_caffeine"]
        try:
            return func(client, db, *args, **kwargs)
        finally:
            client.close()
    return wrapper

# YouTube
@handle_mongodb_connection
def store_in_mongo_youtube(client, db, data, collection_name):
    collection = db[collection_name]
    
    try:
        for record in data:
            video_id = record['video_info']['id']
            existing_record = collection.find_one({"video_info.id": video_id})
            if existing_record:
                # Updating comments for the existing video
                existing_comments = existing_record.get('comments', [])
                new_comments = record['comments']
                # Adding the new comments at the beginning and keep only the top 10 newest comments
                existing_comments = new_comments + existing_comments
                existing_comments = existing_comments[:10]
                record['comments'] = existing_comments
                collection.update_one({"_id": existing_record['_id']}, {"$set": record})
            else:
                # Inserting a new record if it doesn't exist
                collection.insert_one(record)
        print(f"Successfully inserted all records into {collection_name}.\n")
    except Exception as e:
        print(f"An error occurred while inserting records: {e}")

# Reddit
@handle_mongodb_connection
def store_in_mongo_reddit(client, db, data, collection_name):
    collection = db[collection_name]
    
    try:
        for post in data:
            permalink = post.get('permalink')  # Retrieve 'permalink' if it exists
            if permalink:
                existing_post = collection.find_one({"permalink": permalink})
                if existing_post:
                    # Updating comments for the existing post
                    existing_comments = existing_post.get('comments', [])
                    new_comments = post.get('comments', [])  # Getting the new comments from the current post
                    # Filtering out comments that are already present in existing_comments
                    new_comments = [comment for comment in new_comments if comment not in existing_comments]
                    # Combining the existing and new comments and keep only the top 10 newest comments
                    updated_comments = new_comments + existing_comments
                    updated_comments = updated_comments[:10]
                    post['comments'] = updated_comments
                    collection.update_one({"permalink": permalink}, {"$set": post})
                else:
                    # Inserting a new post if it doesn't exist
                    collection.insert_one(post)
        print(f"Successfully inserted records into {collection_name}.\n")
    except Exception as e:
        print(f"An error occurred while inserting records: {e}")

def convert_timestamp_to_est(timestamp):
    # Convert UNIX timestamp to datetime object
    utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
    utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)  # Set the timezone to UTC

    # Convert to Eastern Standard Time (EST)
    est_timezone = pytz.timezone('US/Eastern')
    est_datetime = utc_datetime.astimezone(est_timezone)

    # Format the EST datetime as a string
    est_datetime_str = est_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')

    return est_datetime_str

@handle_mongodb_connection
def get_count(client, db, collection_name):
    collection = db[collection_name]
    post_count = collection.count_documents({})
    cursor = collection.find({})
    comment_count = 0
    for document in cursor:
        comment_count += document['num_comments']
    
    return post_count, comment_count 
#newly added-------------------------------
@handle_mongodb_connection
def get_youtube_count(client, db, collection_name):
    collection = db[collection_name]
    post_count = collection.count_documents({})
    cursor = collection.find({})
    comment_count = 0
    
    for document in cursor:
        comments = document['comments']  # Get the list of comments
        comment_count += len(comments)  # Count the number of comments in the list
    
    return post_count, comment_count


@handle_mongodb_connection
def store_count_mongo(client, db, collection_name, data):
    print(collection_name)
    collection = db[collection_name]
    data['timestamp'] = convert_timestamp_to_est(data['timestamp'])


    collection.insert_one(data)
    print(f"Successfully inserted records into {collection_name}.\n")

def main():
    interval = 10800
    celebrities = [
            "Cristiano Ronaldo",
            "Lionel Messi",
            "Music",
            "Selena Gomez",
            "Kylie Jenner",
            "Dwayne Johnson",
            "Ariana Grande",
            "Gaming",
            "Kim Kardashian",
            "Beyoncé",
            "Taylor Swift",
            "Kendall Jenner",
            "movies"
            # "nfl",
            # "Cricket",
            # "Roel Vandepaar"
        
        ]
    while True:

        #newly added-------------------------------

        yt_prev_p_count , yt_prev_c_count = get_youtube_count('youtube_data')
       

        # Youtube
        youtube_data = []
        for celebrity in celebrities:
            data = fetch_youtube_data(celebrity)
            if data:
                youtube_data.extend(data)

        if youtube_data:
            store_in_mongo_youtube(youtube_data, 'youtube_data')

            #newly added-------------------------------
            yt_current_p_count, yt_current_c_count = get_youtube_count('youtube_data')
            dataset = {
                'timestamp': time.time(),
                'post_count': (yt_current_p_count - yt_prev_p_count),
                'comment_count': (yt_current_c_count - yt_prev_c_count)
            }
            store_count_mongo('store_youtube_count', dataset)

        # new 
        reddit_prev_p_count , reddit_prev_c_count = get_count('reddit_data')

        # Reddit 
        reddit_data = new_reddit_fetch()
        if reddit_data:
            store_in_mongo_reddit(reddit_data,'reddit_data')
            reddit_current_p_count, reddit_current_c_count = get_count('reddit_data')
            dataset = {
                'timestamp': time.time(),
                'post_count': (reddit_current_p_count - reddit_prev_p_count),
                'comment_count': (reddit_current_c_count - reddit_prev_c_count)
            }
            store_count_mongo('store_reddit_count', dataset)

        prev_p_count, prev_c_count = get_count('politics_data')

        # Politics Reddit Data
        politics_data = politics_fetch_data(None, 200)
        if politics_data:
            store_in_mongo_reddit(politics_data, 'politics_data')
            current_p_count, current_c_count = get_count('politics_data')
            datas = {
                'timestamp': time.time(),
                'post_count': (current_p_count - prev_p_count),
                'comment_count': (current_c_count - prev_c_count)
            }
            store_count_mongo('store_count', datas)
        
        
        time.sleep(interval)

if __name__ == "__main__":
    main()