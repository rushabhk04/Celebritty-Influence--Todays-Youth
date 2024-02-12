from flask import Flask, jsonify, render_template, request
import os
from comparative import generate_comparative_plot
from sentiment import plot_toxicity
from influence import plot_influence

app = Flask(__name__)

@app.route('/sentiment_analysis')
def sentiment():
    return render_template('sentiment_analysis.html')

@app.route('/perform_sentiment_analysis', methods=['POST'])
def perform_sentiment_analysis():
    analysis_type = request.form['analysis_type']

    if analysis_type == 'toxicityInMusic':
        subreddit_list = ["Music", "SelenaGomez", "ArianaGrande", "TaylorSwift", "FuckTravisScott"]
        output_file = os.path.join(os.getcwd(), 'static', 'plots', 'sentimentPlots', 'toxicityInMusic.png')
    elif analysis_type == 'toxicityInSports':
        subreddit_list = ["nfl", "CFB", "Cricket", "baseball", "formuladank"]
        output_file = os.path.join(os.getcwd(), 'static', 'plots', 'sentimentPlots', 'toxicityInSports.png')
    elif analysis_type == 'toxicityInTV':
        subreddit_list = ["movies", "netflix", "bollywood", "videos", "Fantasy_Football"]
        output_file = os.path.join(os.getcwd(), 'static', 'plots', 'sentimentPlots', 'toxicityInTV.png')
    else:
        return "Invalid analysis type"

    plot_toxicity(subreddit_list, 'reddit_data', output_file)
    return f"Sentiment analysis completed for {analysis_type}. Check the <a href='/static/plots/sentimentPlots/{analysis_type}.png'>result</a>."

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/comparativeAnalysis")
def comparative_analysis():
    return render_template('comparativeAnalysis.html')


@app.route("/aboutUS")
def aboutUS():
    return render_template('aboutus.html')

@app.route("/generatePlot")
def generate_plot():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    plot_path = generate_comparative_plot(start_date, end_date)
    return jsonify({'plot_path': plot_path})

@app.route("/influence")
def influence():
    return render_template("influence_analysis.html")

@app.route("/report")
def report():
    return render_template("report.html")



@app.route("/allplots")
def allplots():
    return render_template("allplots.html")


@app.route("/peform_influence_analysis", methods=['POST'])
def perform_influence_analysis():
    celeb1 = request.form['celeb1']
    celeb2 = request.form['celeb2']
    subredditList = []
    youtubeList = []

    if celeb1 == 'cristianoronaldo':
        subredditList.append('cristianoronaldo')
        youtubeList.append('Cristiano Ronaldo')
    elif celeb1 == 'SelenaGomez':
        subredditList.append('SelenaGomez')
        youtubeList.append('Selena Gomez')
    elif celeb1 == 'KylieJenner':
        subredditList.append('KylieJenner')
        youtubeList.append('Kylie Jenner')
    elif celeb1 == 'DwayneJohnson':
        subredditList.append('DwayneJohnson')
        youtubeList.append('Dwayne Johnson')
    elif celeb1 == 'KhloeKardash':
        subredditList.append('KhloeKardash')
        youtubeList.append('Khloé Kardashian')
    
    if celeb2 == 'messi':
        subredditList.append('messi')
        youtubeList.append('Lionel Messi')
    elif celeb2 == 'ArianaGrande':
        subredditList.append('ArianaGrande')
        youtubeList.append('Ariana Grande')
    elif celeb2 == 'beyonce':
        subredditList.append('beyonce')
        youtubeList.append('Beyoncé')
    elif celeb2 == 'KimKardashianPics':
        subredditList.append('KimKardashianPics')
        youtubeList.append('Kim Kardashian')
    elif celeb2 == 'kendalljenner':
        subredditList.append('kendalljenner')
        youtubeList.append('Kendall Jenner')

    plot_influence(subredditList, youtubeList)
    return f"Influence analysis completed for influence comparision between {celeb1} and {celeb2}. Check the <a href='/static/plots/influencePlots/influ.png'>result</a>."


if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
