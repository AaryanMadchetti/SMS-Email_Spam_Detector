import streamlit as st
import pickle
import string

import nltk
# nltk.data.path.append("C:\\Users\\Morya\\PycharmProjects\\spam-classifier\\venv\\Lib\\site-packages\\nltk\\tokenize\\punkt.py")  # Ensure this is the correct path
# nltk.download('punkt')
from nltk.corpus import stopwords
stopwords.words('english')

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_input("Enter the Message")

# Preprocessing
transformed_sms = transform_text(input_sms)
# Vectorizing
vector_input = tfidf.fit_transform([transformed_sms])
# Predicting
result = model.predict(vector_input)[0]
# Displaying
if result == 1:
    st.header('Spam!')
else:
    st.header('Not Spam!')
