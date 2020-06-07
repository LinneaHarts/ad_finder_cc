import pickle
import sys
import re, numpy as np, pandas as pd
from pprint import pprint
from nltk.corpus import stopwords

# Gensim
import gensim, spacy, logging, warnings
import gensim.corpora as corpora
from gensim.utils import lemmatize, simple_preprocess
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt

# Scikit Learn
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans




if __name__ == "__main__":
    setup_nltk()
    cnn_df = pd.read_csv('../../data/interim/cnn-last-year-sent-cleaned.csv')
    cnn_df = cnn_df.drop(columns=['Unnamed: 0']).head(1000)
    print(cnn_df.head())
    #vectorizer = CountVectorizer(strip_accents='unicode', stop_words='english', ngram_range=(1,3))
    #vectorizer = TfidfVectorizer(strip_accents='unicode', stop_words='english', min_df=2, max_df=0.3, ngram_range=(1,2))