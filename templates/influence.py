import pymongo
import matplotlib.pyplot as plt


def plot_influence(reddit_list, youtube_list):
    # MongoDB connection
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client["team_caffeine"] 

    youtube_data = db['youtube_data']
    reddit_data = db['reddit_data']
    reddit_count = []
    youtube_count = []
    for celeb in reddit_list:
        temp_count = 0
        for post in reddit_data.find():
            if post['subreddit'] == celeb:
                temp_count += int(post['ups'])
                temp_count += int(post['num_comments'])
        
        reddit_count.append({
            celeb: temp_count
        })

    for ceelb in youtube_list:
        temp_count == 0
        for record in youtube_data.find():
            temp = record['video_info']['statistics']
            if record['Name'] == ceelb:
                if temp.get('likeCount') is not None:
                    temp_count += int(temp['likeCount'])
                if temp.get('commentCount') is not None:
                    temp_count += int(temp['commentCount'])

        youtube_count.append({
            ceelb: temp_count
        })

    print(youtube_count)
    print(reddit_count)

    # Plotting tge graph

    names, count_youtube = extract_data(youtube_count)
    _, count_reddit = extract_data(reddit_count)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.subplot(1, 2, 1)
    plt.bar(names, count_youtube, color=['blue', 'red'])
    plt.title('Influence on youtube')
    plt.ylabel('Celebrity Name')

    plt.subplot(1, 2, 2)
    plt.bar(names, count_reddit, color=['blue', 'red'])
    plt.title('Influence on reddit')
    plt.ylabel('Celebrity Name')

    plt.tight_layout()
    plt.show()
    plt.savefig('./static/plots/influencePlots/influ.png')
    plt.close()


def extract_data(data):
    names = []
    followers = []
    for player_data in data:
        name, follower_count = list(player_data.items())[0]
        names.append(name)
        followers.append(follower_count)
    return names, followers




    
