## Peroject 2 Implementation:-

## Project Abstract
In the digital era, the impact of celebrities on the younger generation is increasingly mediated through social media platforms. This study aims to quantitatively and qualitatively analyze the extent and nature of this influence. Utilizing the APIs of two major social media platforms, YouTube and Reddit, we systematically gather a substantial dataset, which is then meticulously stored in a MongoDB database for robust analysis. Our methodology encompasses a multi-faceted analytical approach, including an Influence Matrix, Trends Analysis, Content Analysis, and Sentiment Analysis, to provide a comprehensive understanding of celebrity impact.

## Team
Bhavit Yogesh Shah bshah5@binghamton.edu
Rushabh Kothari rkothar1@binghamton.edu
Shruti Iyengar siyenga1@binghamton.edu
Mukul Dev mchhang1@binghamton.edu

## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `datetime` - The datetime library used for manipulating dates and times [Python documentation Website]( https://docs.python.org/3/library/datetime.html)
* `Json` - Json is python build in package used to work on JSON data got from different API get request[Python documentation Website](https://docs.python.org/3/library/datetime.html)
* `base64` - base64 is python library used for data encoding [Python documentation Website](https://docs.python.org/3/library/datetime.html)
* `MongoDB` - MongoDB is NoSQL document database used to store data collected from Reddit and YouTube websites [MongoDB Website]( https://www.mongodb.com/)
* `PyMongo` - PyMongo is Python distribution containing tool used to work with MongoDB using Python [PyMongo Website]( https://pymongo.readthedocs.io/en/stable/)

* `MatPlotLib` - We are using this library to generate various plots that are requiered in this part of the project [MatPlotLib Website](https://matplotlib.org/)

* `Natural Language Processing` - We used speech intensity analyzer to analyze the comments and to check if they are positve, neutral or negative. [NLP Speech intensity analyzer](https://github.com/cjhutto/vaderSentiment)

For Installation of different packages:-

Use requirements.txt file(Mentioned in how-to-run steps.)

In this part of the project we perform various analysis based on the data that was collected. Along with this, we also made use of Modern Hate Speech API for toxicity detection. 

We performed four main types of analysis on celebrities and their overall impact:-
1) Comparative
2) Influence 
3) Sentiment
4) timeSeries/trends

 ## How to run the project?

Go inside project-1-implementation-team-caffeine folder:-

1) Using a virtual environment

python3 -m venv venv


2) Activate the virtual environment:

On Linux/macOS:
source venv/bin/activate

On Windows:
. venv/bin/activate

3) Installing all required packages 

python -m pip install --upgrade pip
Use this before installing the below requirements.txt  if  direct install doesn't work 

then,

pip install -r requirements.txt

3) Run the different script 

    1) Comparative
    
    python3 comparative.py
   
    python3 twoData.py
   
    python3 threeData.py
    
    2) Influence 
    
    python3 influence.py
    
    3) Sentiment
    
    python3 sentiment.py
    
    4) timeSeries/trends
    
    python3 trends.py

    For running plot that shows comparison between reddit and youtube in toxicity using --modern hate speech:-
    python3 mhs-plots.py
   
    --for generating politics comments binned hourly 
    python3 politics_comments.py

    **Note:
    We are collecting data for politics subreddit from 3rd of November to 17th November instead of 1st November to 14th November, we had a word with professor during the lecture regarding the same and he approved it.


    All plots will be stored under plots directory. We have run each kind of plot once and stored it just in case. 

    **NOTE: For  data that was to be collected between 1st and 14th. Due to vm problems there is no data on 5th and 6th and some inconsistencies that we had spoken to the professor in class. 

    Other than that we had run the project several times after the vm was restored for testing purposes and that's why you may see a spike on that date. Also, on 17th a spike is seen as after our first demo we were advised to do some changes in scheduling and we tested the same again. 
