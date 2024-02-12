from pymongo import MongoClient
import matplotlib.pyplot as plt

def generate_comparative_plot(start_date, end_date):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['team_caffeine']
    reddit_collection = db['store_reddit_count']
    youtube_collection = db['store_youtube_count']

    # Query Reddit collection for data within the date range
    reddit_data = reddit_collection.find({
        'timestamp': {
            '$gte': start_date,
            '$lte': end_date
        }
    })

    # Query YouTube collection for data within the date range
    youtube_data = youtube_collection.find({
        'timestamp': {
            '$gte': start_date,
            '$lte': end_date
        }
    })

    # Count the number of posts per day for Reddit and YouTube
    reddit_post_count = {}
    youtube_post_count = {}

    for entry in reddit_data:
        date = entry['timestamp'].split()[0]  # Extracting date
        reddit_post_count[date] = reddit_post_count.get(date, 0) + entry['post_count']

    for entry in youtube_data:
        date = entry['timestamp'].split()[0]  # Extracting date
        youtube_post_count[date] = youtube_post_count.get(date, 0) + entry['post_count']

    # Plotting the data
    plt.figure(figsize=(10, 6))

    plt.plot(list(reddit_post_count.keys()), list(reddit_post_count.values()), label='Reddit Posts')
    plt.plot(list(youtube_post_count.keys()), list(youtube_post_count.values()), label='YouTube Posts')

    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.title('Posts Over Time')
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a static folder
    plot_path = f'static/plots/comparativePlots/{start_date}_to_{end_date}.png'
    plt.savefig(plot_path)
    plt.close()

    return plot_path
