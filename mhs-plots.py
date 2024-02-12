from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import time

client = MongoClient('mongodb://localhost:27017/')
db = client["team_caffeine"]

reddit_data_collection = db['reddit_data']
youtube_toxicity_score_collection_name = 'toxicity_score_yt'
youtube_toxicity_score_collection = db[youtube_toxicity_score_collection_name]
toxicity_score_collection_name = 'modernHateSpeech'
toxicity_score_collection = db[toxicity_score_collection_name]
error_collection_name = 'error_mhs'
error_collection = db[error_collection_name]

def plot_toxicity_scores(collections, plot_title):
    plt.figure(figsize=(10, 6))
    dates_data = {}

    for collection, label in zip(collections, ['YouTube', 'Reddit']):
        results = collection.find({}, {"timestamp": 1, "confidence": 1})
        
        
        dates = []
        confidence_scores = []

        for result in results:
            dates.append(result["timestamp"])
            confidence = result.get("confidence")  
            if confidence is not None:
                confidence_scores.append(float(confidence))

        # Converting dates to datetime objects
        dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for date in dates]

        # Here combining dates and confidence scores for each collection
        for date, confidence in zip(dates, confidence_scores):
            key = (date, label)
            dates_data[key] = dates_data.get(key, []) + [confidence]

   
    unique_dates = sorted(set(date for date, label in dates_data.keys()))
    unique_labels = ['YouTube', 'Reddit']

    # Plotting as step CDF chart
    for i, label in enumerate(unique_labels):
        color = 'orange' if label == 'YouTube' else 'blue'
        values = [np.sort(dates_data.get((date, label), [])) for date in unique_dates]
        positions = np.arange(len(unique_dates)) + i
        for value in values:
            plt.step(value, np.linspace(0, 1, len(value)), color=color, where='post', label=f'{label} CDF')

    plt.title(plot_title)
    plt.xlabel('Toxicity Score (Confidence)')
    plt.ylabel('Cumulative Probability')
    
    
    plt.text(0.02, 0.98, 'YouTube - Orange', color='orange', fontsize=10, transform=plt.gca().transAxes, ha='left', va='top')
    plt.text(0.02, 0.93, 'Reddit - Blue', color='blue', fontsize=10, transform=plt.gca().transAxes, ha='left', va='top')

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    plot_filename = f'{plot_title.lower().replace(" ", "_")}_cdf_plot_{current_time}.png'
    plt.savefig(f"plots/mhsPlots/{plot_filename}")
    print(f"Plot saved as {plot_filename}")

    # Show the plot
    plt.show()

def main():
    while True:
        try:
            print("Attempting to plot toxicity scores...")
            plot_toxicity_scores([toxicity_score_collection, youtube_toxicity_score_collection], 'Toxicity Scores CDF Over Time')

            print("Waiting for an hour before checking again...")
            time.sleep(60 * 60)  # Sleep for an hour before checking again
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Waiting for 30 minutes before restarting...")
            time.sleep(30 * 60)  # Sleep for 30 minutes before restarting

if __name__ == "__main__":
    main()
