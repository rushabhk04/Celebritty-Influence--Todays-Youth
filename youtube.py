import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def load_youtube_api_credentials(credentials_file):
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            return credentials.get('api_keys', [])
    except FileNotFoundError:
        logger.error("Credentials file not found. Please check the file path.")
        return []

# Load API keys from the credentials file
API_KEYS = load_youtube_api_credentials('credentials/credentials_youtube.json')

current_api_index = 0

def create_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def fetch_youtube_data(celebrity_name):
    global current_api_index

    print(f"Fetching {celebrity_name}\n")
    try:
        youtube_service = create_youtube_service(API_KEYS[current_api_index])

        video_ids = search_videos(youtube_service, celebrity_name)
        video_data = []

        for video_id in video_ids:
            video_info = get_video_details(youtube_service, video_id)

            if 'commentCount' in video_info['statistics'] and int(video_info['statistics']['commentCount']) > 0:
                comments = get_video_comments(youtube_service, video_id)
            else:
                comments = []

            view_count = get_view_count(video_info)

            video_data.append({
                'Name': celebrity_name,
                'video_info': video_info,
                'comments': comments,
                'view_count': view_count
            })

        return video_data

    except HttpError as e:
        if e.resp.status == 403:  # Rate limit error
            if current_api_index < len(API_KEYS) - 1:
                current_api_index += 1
                logger.info(f"Switching to API key index {current_api_index}")
                return fetch_youtube_data(celebrity_name)
            else:
                logger.error("All API keys reached their limits")
                return []
        else:
            logger.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return []

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

def search_videos(youtube_service, celebrity_name):
    search_response = youtube_service.search().list(
        q=celebrity_name,
        type="video",
        part="id",
        maxResults=100
        # order="viewCount"  # Sort by view count in descending order
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    return video_ids

def get_video_details(youtube_service, video_id):
    video_response = youtube_service.videos().list(
        id=video_id,
        part="snippet,statistics"
    ).execute()

    video_info = video_response.get('items', [])[0]
    return video_info

def get_video_comments(youtube_service, video_id):
    comment_threads = youtube_service.commentThreads().list(
        videoId=video_id,
        part="snippet",
        textFormat="plainText",
        maxResults=20
    ).execute()

    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay']
                for item in comment_threads.get('items', [])]

    return comments

def get_view_count(video_info):
    statistics = video_info.get('statistics', {})
    view_count = statistics.get('viewCount', 0)
    return view_count