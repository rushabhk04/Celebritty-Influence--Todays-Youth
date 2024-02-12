import pymongo
import requests
import time
from datetime import datetime

# ModerateHatespeech API details
api_url = "https://api.moderatehatespeech.com/api/v1/moderate/"
api_key = 'aca5c1785b374e79f17b874d6726c09d'

# MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["team_caffeine"]
reddit_data_collection = db['reddit_data']

toxicity_score_collection_name = 'modernHateSpeech'
toxicity_score_collection = db[toxicity_score_collection_name]
error_collection_name = 'error_mhs'
error_collection = db[error_collection_name]

def send_toxicity_request(comment_text):
    
    payload = {
        "token": api_key,
        "text": comment_text,
    }

    
    headers = {
        "Content-Type": "application/json"
    }

    
    response = requests.post(api_url, json=payload, headers=headers)

   
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error sending toxicity request: {response.status_code}, {response.text}")
        return None

def send_toxicity_request_with_retry(comment_text):
    max_retries = 3
    delay_seconds = 1
    retries = 0
    while retries < max_retries:
        try:
            return send_toxicity_request(comment_text)
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(delay_seconds)
            retries += 1
    else:
        print("Max retries reached. Could not send toxicity request.")
        return None

def process_and_store_in_mongodb(start_id):
    
    from bson.objectid import ObjectId

    query = {"_id": {"$gt": ObjectId(start_id)}}
    reddit_data = reddit_data_collection.find(query)

    
    for document in reddit_data:
        comments = document.get("comments", [])
        for comment in comments:
            comment_text = comment.get("comment_text", "")

            
            api_response = send_toxicity_request_with_retry(comment_text)

            if api_response:
                result_entry = {
                    "comment_text": comment_text,
                    "response": api_response.get("response"),
                    "class": api_response.get("class"),
                    "confidence": api_response.get("confidence"),
                    "timestamp": datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                }
                toxicity_score_collection.update_one(
                    {"comment_text": result_entry["comment_text"]},
                    {"$set": result_entry},
                    upsert=True
                )
            else:
                error_entry = {
                    "comment_text": comment_text,
                    "timestamp": datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "error_message": "Max retries reached. Could not send toxicity request."
                }
                error_collection.insert_one(error_entry)

def main():
    
    start_id = "65634ee5225a9feb61e202c9"

    while True:
        try:
            process_and_store_in_mongodb(start_id)
            time.sleep(60 * 60)  # Sleep for an hour before checking again
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30 * 60)  # Sleep for 30 minutes before restarting

if __name__ == "__main__":
    main()
