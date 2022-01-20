# Contraviz - A Global COVID19 Trend Tracking Visualizer

## Project Overview
* Created an end-to-end webapp for real-time data analytics on COVID-19 to gain insights into the COVID19 trends and identified the sentiment of people towards the vaccination drive across the globe
* Visualized and incorporated descriptive models including heat maps, geographic maps, bar charts and line charts for representing different statistics of the COVID-19 outbreak into the webapp using Plotly
* Performed sentiment analysis of vaccination tweets using Natural Language Processing methodologies to extract key features using libraries Tf-IDK Vectorizer, textblob, NLTK and Spacy and built subsequent machine learning models using Naive Bayes and LSTM
* Deployed the webapp on Heroku, presented and published the findings in a research paper[link](https://www.annalsofrscb.ro/index.php/journal/article/view/2826)

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, numpy, plotly, dash, <br />
**Requirements:** ```pip install -r requirements.txt``` 

# Objective A : Analysis of COVID19 cases

## Data Collection
* The dataset for COVID19 cases is acquired from the Johns Hopkins University's Center for Systems Science and Engineering - GitHub repository. It includes recovered cases, confirmed cases, and deaths updated daily.
* For sentiment analysis, the dataset called "All COVID-19 Vaccines Tweets" was fetched from Kaggle. This dataset is updated daily with new tweets regarding COVID-19 vaccines like Pfizer/BioNTech, Sinopharm, Sinovac, Moderna, Covaxin, Sputnik V and Oxford/AstraZeneca. 

# Objective B : Sentiment Analysis of Vaccination tweets

## Data Collection
For sentiment analysis, the dataset called "All COVID-19 Vaccines Tweets" was fetched from Kaggle. This dataset is updated daily with new tweets regarding COVID-19 vaccines like Pfizer/BioNTech, Sinopharm, Sinovac, Moderna, Covaxin, Sputnik V and Oxford/AstraZeneca. 
 
## Preprocessing and Feature Engineering
The preprocessing stage consists of a variety of steps:-
* All uppercase letters can be converted to lowercase.
* Tokenization is the process of removing the hashtags,  numbers, URL's and targets (@). Hashtags were removed from the tweet text, but a separate column was created to store them. NLTK Module was used to tokenize all tweets.
* Stemming has also been performed. This helps reduce words to their root form. Words that are not in English are removed. We are primarily interested in English tweets, so non-English words have been removed.
* Removal of stop words - Stop words have a negative impact on emotion recognition, so they must be eliminated. 

The preprocessed tweet is converted to a feature vectors that can be used to determine the importance of a word in a collection or corpus.

## Model Building 
* Naive Bayes classifier: A  Naive Bayes  classifier assumes  that  the presence  of  a  particular feature  in  a  class is unrelated to the presence of any other feature.
The final XGB model was then trained on the whole training dataset using the hyperparameters found in the Optuna experiment.

## Productionization
A webapp was built on DASH [DASH app](https://contraviz.herokuapp.com/) that is hosted publicly using Heroku.
