import pymongo
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt



def plot_toxicity(subreddits, collection_name, output_file):
    # Initializing SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

    # MongoDB connection
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client["team_caffeine"] 
    reddit_data_collection = db[collection_name]

    subreddit_scores = {subreddit: {"positive": 0, "neutral": 0, "negative": 0} for subreddit in subreddits}

    for document in reddit_data_collection.find():
        subreddit = document.get("subreddit")
        if subreddit in subreddits:
            comments = document.get("comments", [])
            for comment in comments:
                comment_text = comment.get("comment_text", "")
                
                # sentiment analysis on each comment
                scores = sid.polarity_scores(comment_text)
                
                if scores['compound'] > 0.5:
                    subreddit_scores[subreddit]["positive"] += 1
                elif 0 <= scores['compound'] <= 0.5:
                    subreddit_scores[subreddit]["neutral"] += 1
                else:
                    subreddit_scores[subreddit]["negative"] += 1

    # Plotting
    for i, (subreddit, scores) in enumerate(subreddit_scores.items()):
        plt.bar(subreddit, scores["positive"], color='green', label='Positive' if i == 0 else None)
        plt.bar(subreddit, scores["neutral"], bottom=scores["positive"], color='yellow', label='Neutral' if i == 0 else None)
        plt.bar(subreddit, scores["negative"], bottom=scores["positive"] + scores["neutral"], color='red', label='Negative' if i == 0 else None)

    plt.xlabel('Subreddits')
    plt.ylabel('Toxicity Levels')
    plt.title('Toxicity Levels In Reddit')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.legend()
    plt.savefig(output_file)
    plt.show()
    plt.close()

def main():
    subreddit_list_1 = ["Music", "SelenaGomez", "ArianaGrande", "TaylorSwift", "FuckTravisScott"]
    subreddit_list_2 = ["nfl", "CFB", "Cricket", "baseball", "formuladank"]
    subreddit_list_3 = ["movies", "netflix", "bollywood", "videos", "Fantasy_Football"]

    plot_toxicity(subreddit_list_1, 'reddit_data', 'plots/sentimentPlots/toxicityInMusic.png')
    plot_toxicity(subreddit_list_2, 'reddit_data', 'plots/sentimentPlots/toxicityInSports.png')
    plot_toxicity(subreddit_list_3, 'reddit_data', 'plots/sentimentPlots/toxicityInTV.png')


if __name__ == "__main__":
    main()
