from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np

client = MongoClient('mongodb://localhost:27017/')
db = client["team_caffeine"]

reddit_data_collection = db['store_reddit_count']
youtube_data_collection = db['store_youtube_count']

def plot(collections):
    plt.figure(figsize=(10, 6))
    dates_data = {}

    for collection, label in zip(collections, ['YouTube', 'Reddit']):
        results = collection.find({}, {"timestamp": 1, "post_count": 1})
        
        dates = []
        post_counts = []

        for result in results:
            target_day = datetime(2023, 11, 17)
            ts = result['timestamp']
            current_ts = parser.parse(ts)
            if current_ts >= target_day:
                dates.append(result["timestamp"])
                post_count = result.get("post_count")
                if post_count is not None:
                    post_counts.append(int(post_count))

        # Converting dates to datetime objects
        dates = [parser.parse(date).replace(tzinfo=None).strftime('%Y-%m-%d') for date in dates]
        # Combining dates and comment counts for each collection
        for date, count in zip(dates, post_counts):
            key = (date, label)
            dates_data[key] = dates_data.get(key, []) + [count]

    unique_dates = sorted(set(date for date, label in dates_data.keys()))
    unique_labels = ['YouTube', 'Reddit']

    # Plotting as a line chart with a logarithmic y-axis scale
    for i, label in enumerate(unique_labels):
        color = 'orange' if label == 'YouTube' else 'green'
        values = [np.mean(dates_data.get((date, label), [])) for date in unique_dates]
        plt.plot(unique_dates, values, color=color, label=f'{label} Posts')

    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.title('Post Counts Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Number of Posts (log scale)')
    plt.legend(loc='upper right', fontsize='small')  # Change legend position and font size
    plt.xticks(rotation=45)
    plt.tight_layout()

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(f"plots/comparativePlots/PostCounts.png")
    plt.show()

def main():
    plot([youtube_data_collection, reddit_data_collection])

if __name__ == "__main__":
    main()
