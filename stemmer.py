import csv
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import math


def setup(fname):
    """
    This function is specific to me because I'm loading in files in this directory
    """
    with open(fname) as f:
        articles=[{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        for article in articles:
            article['text']=clean_string(article['text'])
    with open(fname, 'w') as f:
            column_names = sorted(articles[0].keys())
            new_f = csv.DictWriter(f, column_names)
            new_f.writeheader()
            new_f.writerows(articles)

def clean_string(text):
    """
    Helper function that takes in an article text as a string
    Returns: new string with article text cleaned up, punctuation and stop words removed
    """
    ps = PorterStemmer()
    punct = '?.,!\n1234567890'
    useless_words = {'mr', 'mrs', 'ms', 'dr', 'said', 'says', "new",'yorker', 'yorkers','york', 'city', 'de', 'blasio', 'council', 'bill', 'mayor', 'quinn', 'bloomberg'}
    text = text.lower()
    for p in punct:
        text = text.replace(p, ' ')
    stop_words = set(stopwords.words('english'))|useless_words
    word_tokens = word_tokenize(text)
    new_text = ''
    for token in word_tokens:
        if len(token) > 1 and token not in stop_words:
            new_text += ps.stem(token)+' '
    return new_text.strip()

for y in range(2013, 2020):
    year = str(y)
    setup('New_Articles_'+year+'.csv')
