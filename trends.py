from pymongo import MongoClient
from datetime import datetime
import pytz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np  


def aggregate_daily_view_counts(db, target_date):
    daily_view_counts = {}

    collection = db['youtube_data']
    video_records = collection.find()

    for record in video_records:
        published_timestamp = record['video_info']['snippet']['publishedAt']
        view_count = int(record['video_info']['statistics'].get('viewCount', 0))

        published_datetime = datetime.strptime(published_timestamp, '%Y-%m-%dT%H:%M:%SZ')
        published_date = published_datetime.date()

        if published_date >= target_date:
            if published_date in daily_view_counts:
                daily_view_counts[published_date].append(view_count)
            else:
                daily_view_counts[published_date] = [view_count]

    return daily_view_counts


def create_daily_view_count_cdf(daily_view_counts):
    view_counts = []
    for date in daily_view_counts.values():
        view_counts.extend(date)

    view_counts.sort()
    n = len(view_counts)
    cumulative = np.arange(1, n + 1) / n

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlabel('View Count')
    ax.set_xscale('log')
    ax.set_ylabel('CDF')
    ax.set_title('Cumulative Distribution Function of Daily View Counts')

    ax.plot(view_counts, cumulative, marker='.', linestyle='none')
    ax.grid()

    plt.tight_layout()
    plt.savefig(f'plots/timeSeries/daily_view_cdf.png')
    plt.close()


def generate_and_plot_average_post_count(collection, output1, output2, target_date):
    pipeline = [
        {
            "$project": {
                "timestamp": {
                    "$dateFromString": {
                        "dateString": "$timestamp",
                        "format": "%Y-%m-%d %H:%M:%S %z"
                    }
                },
                "comment_count": 1,
                "post_count" : 1
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"}
                },
                "avg_comment_count": {"$sum": "$comment_count"},
                "avg_post_count": {"$sum": "$post_count"}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    dates = []
    avg_comment_counts = []
    avg_post_counts = []

    for entry in result:
        year = entry["_id"]["year"]
        month = entry["_id"]["month"]
        day = entry["_id"]["day"]
        date = datetime(year, month, day, tzinfo=pytz.timezone('US/Eastern'))

        if date.date() >= target_date:
            dates.append(date)
            avg_comment_counts.append(entry["avg_comment_count"])
            avg_post_counts.append(entry["avg_post_count"])

    plt.bar(dates, avg_comment_counts)
    plt.xlabel('Date')
    plt.ylabel('Comment Count')
    plt.title('Comment Count by Day')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(output1)
    plt.close()

    plt.bar(dates, avg_post_counts)
    plt.xlabel('Date')
    plt.ylabel('Post Count')
    plt.title('Post Count by Day')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(output2)
    plt.close()


if __name__ == '__main__':
    target_date = datetime(2023, 11, 17).date()
    client = MongoClient('mongodb://localhost:27017/')
    db = client["team_caffeine"]

    collection_name = 'store_count'
    collection = db[collection_name]
    generate_and_plot_average_post_count(collection, "plots/timeSeries/politicsComments.png","plots/timeSeries/politicsPosts.png", target_date)
    
    collection_name = 'store_reddit_count'
    collection = db[collection_name]
    generate_and_plot_average_post_count(collection, "plots/timeSeries/redditCommets.png", "plots/timeSeries/redditPosts.png", target_date)

    daily_view_counts = aggregate_daily_view_counts(db, target_date)
    create_daily_view_count_cdf(daily_view_counts)

    client.close()
