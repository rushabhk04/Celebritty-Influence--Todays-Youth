import pymongo
from pymongo import MongoClient
import requests
import time
from datetime import datetime

# ModerateHatespeech API details
api_url = "https://api.moderatehatespeech.com/api/v1/moderate/"
api_key = 'aca5c1785b374e79f17b874d6726c09d'

    # MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["team_caffeine"]
youtube_data_collection = db['youtube_data']
toxicity_score_collection_name = 'toxicity_score_yt'
toxicity_score_collection = db[toxicity_score_collection_name]
error_collection_name = 'error_toxicity_score_yt'
error_collection = db[error_collection_name]

def send_toxicity_request(comment):
    payload = {
        "token": api_key,
        "text": comment,
    }

   
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error sending toxicity request: {response.status_code}, {response.text}")
        return None

def send_toxicity_request_with_retry(comment):
    max_retries = 3
    delay_seconds = 1
    retries = 0
    while retries < max_retries:
        try:
            return send_toxicity_request(comment)
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(delay_seconds)
            retries += 1
    else:
        print("Max retries reached. Could not send toxicity request.")
        return None

def process_and_store_in_mongodb():
    
    
    current_hour = time.strftime("%Y%m%d%H")
    new_collection_name = f'youtube_data_{current_hour}'
    new_collection = db[new_collection_name]

    # Iterating over MongoDB collection
for document in youtube_data_collection.find():
    # Extract comments array from the document
    comments = document.get("comments", [])

    
    for comment in comments:
        # Sending the comment text to the ModerateHatespeech API with retries
        api_response = send_toxicity_request_with_retry(comment)

        
        if api_response:
            result_entry = {
                "comment_text": comment,
                "response": api_response.get("response"),
                "class": api_response.get("class"),
                "confidence": api_response.get("confidence"),
                "timestamp": datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            toxicity_score_collection.insert_one(result_entry)
        else:
            
            error_entry = {
                "comment_text": comment,
                "timestamp": datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                "error_message": "Max retries reached. Could not send toxicity request."
            }
            error_collection.insert_one(error_entry)


def main():
    while True:
        try:
            print("Running job for 2 minutes...")
            # Run the job for 2 minutes
            start_time = time.time()
            while time.time() - start_time < 2 * 60:
                process_and_store_in_mongodb()

        except Exception as e:
            print(f"An error occurred: {e}")
            
            # Sleep for 30 minutes before restarting the entire process
            print("Restarting after 30 minutes...")
            time.sleep(30 * 60)  # Sleep for 30 minutes before restarting

if __name__ == "__main__":
    main()
