# Importing the libraries
from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# seed for reproducibility of results
np.random.seed(0)

# Importing the dataset
train_set = pd.read_csv('train.tsv', delimiter='\t')
raw_docs_train = train_set['Phrase'].values
sentiment_train = train_set['Sentiment'].values
num_labels = len(np.unique(sentiment_train))

# 1. SGD CLassifier
# text pre-processing

corpus = []

for i in range(len(raw_docs_train)):
    review = re.sub('[^a-zA-Z]', ' ', raw_docs_train[
        i])  # remove numbers and punctuations (don't remove letters a-z and A-Z) and second parameter ' ' is used to replace the removed character by a space.
    review = raw_docs_train[i].lower()  # convert all letters to lowercase
    review = review.split()  # convert the review into a list of different words of the review.

    ps = PorterStemmer()  # Stemming process to keep only the root of the word i.e. keep 'love' and not 'loved'
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}'])
    review = [ps.stem(word) for word in review if
              not word in stop_words]  # retain only those english words in the list that are not present in stopwords. 'set' is used to make the algo faster because python goes through a set faster than a list

    review = ' '.join(review)  # convert the list of words back to a single string of words.
    if review == '' or review == ' ':
        review = 'neutral'

    corpus.append(review)

from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'
app.secret_key = "jose"


@app.route('/')
def home_template():
    return render_template("home.html")

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = "Oops! Id and Password do not match"

    return render_template("user_blogs.html", email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("login.html", email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, user._id)
        new_blog.save_to_mongo()

        new_title = title.replace(" ", "_") # to be able to use it in the url
        my_url = "https://www.rottentomatoes.com/m/" + new_title + "/reviews/"
        # case sensitivity in url gets corrected automatically by browser

        # obtain the reviews of the required movie
        req = requests.get(my_url)
        content = req.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find_all("div", {"class": "the_review"})

        if len(element) == 0:
            new_url = req.url + "/reviews/"
            req = requests.get(new_url)
            content = req.content
            soup = BeautifulSoup(content, "html.parser")
            element = soup.find_all("div", {"class": "the_review"})

        # preparing test set
        test_set_reviews = []
        for i in range(len(element)):
            test_set_reviews.append(element[i].text)

        corpus2 = []

        for i in range(len(test_set_reviews)):
            review = re.sub('[^a-zA-Z]', ' ', test_set_reviews[i])  # remove numbers and punctuations (don't remove letters a-z and A-Z) and second parameter ' ' is used to replace the removed character by a space.
            review = test_set_reviews[i].lower()  # convert all letters to lowercase
            review = review.split()  # convert the review into a list of different words of the review.

            ps = PorterStemmer()  # Stemming process to keep only the root of the word i.e. keep 'love' and not 'loved'
            stop_words = set(stopwords.words('english'))
            stop_words.update(['.', ',', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}'])
            review = [ps.stem(word) for word in review if not word in stop_words]  # retain only those english words in the list that are not present in stopwords. 'set' is used to make the algo faster because python goes through a set faster than a list

            review = ' '.join(review)  # convert the list of words back to a single string of words.
            if review == '' or review == ' ':  # sometimes, after applying
                review = 'neutral'

            corpus2.append(review)

        if len(corpus2) == 0: # if no reviews found
            return "Sorry! No reviews yet for this movie. Please check spelling or try some other movie."

        # create the bag of words
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        x_train = vectorizer.fit_transform(corpus)
        x_train = x_train.astype('float16')

        x_test = vectorizer.transform(corpus2)
        x_test = x_test.astype('float16')

        # fitting SGD Classifier
        from sklearn.linear_model import SGDClassifier

        classifier_sgd = SGDClassifier(loss='hinge', shuffle=True, penalty='elasticnet', alpha=0.00001)
        classifier_sgd.fit(x_train, sentiment_train)

        # predict
        y_pred_sgd = classifier_sgd.predict(x_test)

        res = 0
        for i in range(len(y_pred_sgd)):
            if y_pred_sgd[i] == 4:
                y_pred_sgd[i] = 3
            elif y_pred_sgd[i] == 0:
                y_pred_sgd[i] = 1

        for i in range(len(y_pred_sgd)):
            if y_pred_sgd[i] == 1:
                res+=0
            elif y_pred_sgd[i] == 2:
                res+=50
            else:
                res+=100
        rate = res/(len(y_pred_sgd))
        rate = str(rate)

        from collections import Counter
        data = Counter(y_pred_sgd)
        ans = data.most_common(1)[0][0]  # Returns the highest occurring item

        if ans == 1:
            return "Negative Reviews!! Drop this Movie. " + "rating is : " + rate
        elif ans == 2:
            return "Neutral Reviews!! Go at your own risk. :) " + "rating is : " + rate
        elif ans == 3:
            return "Positive Reviews!! Go for it. " + "rating is : " + rate
        else:
            return "Sorry! Some Error in Processing"

if __name__ == '__main__':
    app.run(port=4995, debug=True)
