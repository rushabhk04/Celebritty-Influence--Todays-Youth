from pymongo import MongoClient
from datetime import datetime, timedelta
import re  
import matplotlib.pyplot as plt
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
def get_like_counts_reddit(client, db, subreddit, i):
    collection = db[subreddit]
    post_record = collection.find()
    target_day = datetime(2023, 11, i)
    hourly_counts = {}

    for post in post_record:
        ts = post['timestamp']

        # Remove time zone abbreviation 'EDT' or 'EST'
        ts = re.sub(r'\s(EDT|EST)$', '', ts)

        try:
            timestamp = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            print(f"Error parsing timestamp {ts}: {e}")
            continue

        if timestamp.date() == target_day.date():
            hour_start = datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, 0, 0)
            if hour_start not in hourly_counts:
                hourly_counts[hour_start] = 0
            hourly_counts[hour_start] += post['comment_count']

    return hourly_counts



def start_count():
    reddit_count = []
    for i in range(1, 17):
        reddit_count.append(get_like_counts_reddit('store_count', i))
    plot_data(reddit_count)

def plot_data(data):
    x_data = []
    y_data = []
    for hourly_counts in data:
        x_data.extend(list(hourly_counts.keys()))
        y_data.extend(list(hourly_counts.values()))

    plt.figure(figsize=(15, 10))
    plt.plot(x_data, y_data, color='blue')  # Plot the comment counts

    plt.gca().xaxis_date()
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Date')
    plt.ylabel('Comment Count')
    plt.title('Politics Comment Counts Binned hourly')

    t = time.time()
    plt.savefig(f'plots/timeSeries/politicsPlotComment_{time.ctime(t)}.png')
    plt.show()

if __name__ == "__main__":
    start_count()
