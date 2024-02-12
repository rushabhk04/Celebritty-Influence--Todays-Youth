## Project 3 Implementation:-

## Project Abstract
In the digital era, the impact of celebrities on the younger generation is increasingly mediated through social media platforms. This study aims to quantitatively and qualitatively analyze the extent and nature of this influence. Utilizing the APIs of two major social media platforms, YouTube and Reddit, we systematically gather a substantial dataset, which is then meticulously stored in a MongoDB database for robust analysis. Our methodology encompasses a multi-faceted analytical approach, including an Influence Matrix, Trends Analysis, Content Analysis, and Sentiment Analysis, to comprehensively understand celebrity impact.

## Team
Bhavit Yogesh Shah bshah5@binghamton.edu
Rushabh Kothari rkothar1@binghamton.edu
Shruti Iyengar siyenga1@binghamton.edu
Mukul Dev mchhang1@binghamton.edu

## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
*  `flask` - This tool is used to create a web-based framework where we will be showing the interactive way of working with the analysis. [Flask_Website](https://github.com/pallets/flask)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `datetime` - The datetime library used for manipulating dates and times [Python documentation Website]( https://docs.python.org/3/library/datetime.html)
* `Json` - Json is python build in package used to work on JSON data got from different API get request[Python documentation Website](https://docs.python.org/3/library/datetime.html)
* `base64` - base64 is python library used for data encoding [Python documentation Website](https://docs.python.org/3/library/datetime.html)
* `MongoDB` - MongoDB is NoSQL document database used to store data collected from Reddit and YouTube websites [MongoDB Website]( https://www.mongodb.com/)
* `PyMongo` - PyMongo is Python distribution containing tool used to work with MongoDB using Python [PyMongo Website]( https://pymongo.readthedocs.io/en/stable/)

* `MatPlotLib` - We are using this library to generate various plots that are requiered in this part of the project [MatPlotLib Website](https://matplotlib.org/)

* `Natural Language Processing` - We used speech intensity analyzer to analyze the comments and to check if they are positve, neutral or negative. [NLP Speech intensity analyzer](https://github.com/cjhutto/vaderSentiment)

For Installation of different packages:-

Use req.txt file(Mentioned in how-to-run steps.)

In this part of the project we have developed an interactive tool including various analysis based on the data that was collected. All the HMTL files should be under templates folder

The code structure :-

1-app.py- This file contains code which is based on the flask modules. By running this file, it activates routes to different analysis given below.
2-comparative.py- This file contains code which is based on the number of posts from Reddit and YouTube and here the comparison is made. 
3-influence.py- This file contains code which connects to MongoDB and generate plots based on the likes, comments for various celebrities for Reddit and YouTube.
4-sentiment.py- This file contains code which is using NLTK technique for NLP to find toxicity and influence of celebrities on people life's for generes such as music, entertainment and sports. 
5- static folder contains images, plots and styles used in our website. 
6- template contains html files for all the three analysis. 

We performed three main types of analysis on celebrities and their overall impact:-
1) Comparative
2) Influence 
3) Sentiment

 ## How to run the project?

Go inside project-3-implementation-team-caffeine folder:-

1) Using a virtual environment

python3 -m venv venv


2) Activate the virtual environment:

On Linux/macOS:
source venv/bin/activate

On Windows:
. venv/bin/activate

3) Installing all required packages 

python -m pip install --upgrade pip
Use this before installing the below req.txt  if  direct install doesn't work 

then,

pip install -r req.txt

3) Run the different script 

    1) For start of an interactive website or for waking up the server, use command

    python3 app.py

    This will open a website on host and port http://127.0.0.1:5000/

    Now for below analysis: 

    1) Comparative
    
    http://127.0.0.1:5000/comparativeAnalysis
    
    2) Influence 

    http://127.0.0.1:5000/influence


    3) Sentiment
    
    http://127.0.0.1:5000/sentiment_analysis


    For running all the plots that shows comparison between reddit and youtube :-

    4) General Plots

     http://127.0.0.1:5000/generatePlot
   

    **Note:
    
    In our MongoDB database, we have have collected data from 3rd November to 27th November for the toxicity and sentiment based data.All plots will be stored under static/plots directory. We have run each kind of plot once and stored it just in case. Also, the images that will be used in our website, are also stored under path static/images. 
