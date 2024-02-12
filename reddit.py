import requests
import json

# Initialize the index for API key selection
index = 0

def load_reddit_api_credentials(credentials_file):
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            return credentials.get('api_keys', [])
    except FileNotFoundError:
        print("Credentials file not found. Please check the file path.")
        return []

# Load API keys from the credentials file
API_KEYS = load_reddit_api_credentials('credentials/credentials_reddit.json')

def get_reddit_auth_header():
    global index
    # Retrieve API key based on index
    CLIENT_ID = API_KEYS[index]['client_id']
    SECRET_KEY = API_KEYS[index]['secret_key']

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': 'bhavit32',
        'password': 'Crawler@123'
    }
    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
    return headers


def fetch_post_comments(permalink):
    comments = []
    headers = get_reddit_auth_header()
    # Build the URL for the post's comments
    comments_url = f'https://oauth.reddit.com{permalink}.json'

    # Set the parameters for the request
    
    try:
        res = requests.get(comments_url, headers=headers)
        response_data = res.json()

        # Check if the response data is a list and not empty
        if isinstance(response_data, list) and len(response_data) > 0:
            # Extract the comments from the response
            post_data = response_data[1]['data']['children']
            for item in post_data:
                if item['kind'] == 't1':
                    comment = item['data']
                    if 'body' in comment:
                        comment_data = {
                            'id': comment['id'],
                            'subreddit': comment['subreddit'],
                            'comment_text': comment['body'],
                        }
                        comments.append(comment_data)
    except:
        if res.status_code == 429:
            global index
            index = (index + 1) % 3
            comments = fetch_post_comments(permalink)
            return comments
    return comments


def fetch_data(celebrity_name):

    print(f"Fetching {celebrity_name}\n")
    headers = get_reddit_auth_header()
    params = {
        'limit': 100
        # 'sort': 'top'
    }
    dataset = []
    try:
        res = requests.get(f'https://oauth.reddit.com/r/{celebrity_name}/hot', headers = headers, params=params)
        
        for post in res.json()['data']['children']:
            comments = fetch_post_comments( post['data']['permalink'])
            dataset.append({
                'id': post['data']['id'],
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['subreddit'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score'],
                'num_comments': post['data']['num_comments'],
                'permalink': post['data']['permalink'],
                'comments': comments
            })
    except:
        if res.status_code == 429:
            global index
            index = (index + 1) % 3
            dataset = fetch_data(celebrity_name)
            return dataset
    
    # print (dataset[-1])
    return dataset



def new_reddit_fetch():
    celebrities = [
            "Entertainment",
            "fut",
            "netflix",
            "Music",
            "videos",
            "pics",
            "nfl",
            "CFB",
            "memes",
            "bollywood",
            "Fitness",
            "TikTok",
            "Cricket",
            "baseball",
            "formuladank",
            "SelenaGomez",
            "KylieJenner",
            "hiphopheads",
            "ArianaGrande",
            "KimKardashianPics",
            "Fantasy_Football",
            "TaylorSwift", 
            "KendallJenner",
            "bangtan",
            "movies",
            "FuckTravisScott",
            "celebrities"
        ]
    all_data = []  # List to store data for all celebrities
    
    for celebrity in celebrities:
        subData = fetch_data(celebrity)  # Fetch data for the current celebrity
        all_data.extend(subData)  # Add the data to the list
        
    return all_data



# Code to fetch data from the politics subreddit


def fetch_post_comments_politics(permalink):
    comments = []
    headers = get_reddit_auth_header()
    # Build the URL for the post's comments
    comments_url = f'https://oauth.reddit.com{permalink}.json'

    # Set the parameters for the request
    
    try:
        res = requests.get(comments_url, headers=headers)
        response_data = res.json()
        # Check if the response data is a list and not empty
        if isinstance(response_data, list) and len(response_data) > 0:
            # Extract the comments from the response
            post_data = response_data[1]['data']['children']
            for item in post_data:
                if item['kind'] == 't1':
                    comment = item['data']
                    if 'body' in comment:
                        comment_data = {
                            'id': comment['id'],
                            'subreddit': comment['subreddit'],
                            'comment_text': comment['body'],
                        }
                        comments.append(comment_data)
    except:
        if res.status_code == 429:
            global index
            index = (index + 1) % 3
            comments = fetch_post_comments(permalink)
            return comments

    return comments


def politics_fetch_data(after, limit):
    print("Fetching from politics\n")
    headers = get_reddit_auth_header()
    dataset = []
    
    try:
        for _ in range(2):  # Fetch multiple sets of posts (you can adjust this range)
            params = {'limit': limit}
            if after:
                params['after'] = after
            
            res = requests.get('https://oauth.reddit.com/r/politics/new?limit={limit}', headers=headers, params=params)
            
            if res.status_code == 429:
                global index
                index = (index + 1) % 3
                dataset = politics_fetch_data()
                return dataset
            
            data = res.json()['data']['children']
            for post in data:
                comments = fetch_post_comments_politics(post['data']['permalink'])
                dataset.append({
                    'id': post['data']['id'],
                    'subreddit': post['data']['subreddit'],
                    'title': post['data']['title'],
                    'selftext': post['data']['selftext'],
                    'upvote_ratio': post['data']['subreddit'],
                    'ups': post['data']['ups'],
                    'downs': post['data']['downs'],
                    'score': post['data']['score'],
                    'num_comments': post['data']['num_comments'],
                    'permalink': post['data']['permalink'],
                    'comments': comments
                })
            
            after = res.json()['data']['after']
            
            # Call politics_fetch_data recursively with the new 'after' parameter for the next page
            if not after:
                break  # Break if there are no more pages
            
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
    
    return dataset


if __name__ == "__main__":
    new_reddit_fetch()
    politics_fetch_data()