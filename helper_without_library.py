import requests
import json
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import unittest
import csv

API_KEY = 'U4XXY5ozk9hpOMIJEAaLAFWPk9Wui5Cl'
CURRENT_COUNCIL_MEMBERS = {18: 'Ruben Diaz', 42: 'Inez Barron', 14: 'Fernando Cabrera', 1: 'Margaret Chin', 11: 'Andrew Cohen', 36: 'Robert Cornegy', 22: 'Costa Constantinides', 30: 'Robert Holden', 35: 'Laurie Cumbo', 48: 'Chaim M. Deutsch', 25: 'Daniel Dromm', 37: 'Rafael Espinal', 40: 'Mathieu Eugene', 4: 'Keith Powers', 43: 'Justin Brannan', 16: 'Vanessa L Gibson', 44: 'Kalman Yeger', 3: 'Corey Johnson', 12: 'Andy King', 5: 'Ben Kallos', 20: 'Peter Koo', 29: 'Karen Koslowitz', 24: 'Rory Lancman', 39: 'Brad Lander', 33: 'Stephen Levin', 7: 'Mark Levine', 46: 'Alan Maisel', 8: 'Diana Ayala', 50: 'Steven Matteo', 41: 'Alicka Ampry-Samuel', 38: 'Carlos Menchaca', 2: 'Carlina Rivera', 27: 'I. Daneek Miller', 31: 'Donovan Richards', 10: 'Ydanis Rodriguez', 49: 'Deborah Rose', 6: 'Helen Rosenthal', 15: 'Ritchie Torres', 47: 'Mark Treyger', 32: 'Eric Ulrich', 13: 'Mark Gjonaj', 19: 'Paul Vallone', 26: 'Jimmy Van Bramer', 45: 'Farah Louis', 21: 'Francisco Moya', 28: 'Adrienne Adams', 51: 'Joseph Borelli', 34: 'Antonio Reynoso', 9: 'Bill Perkins', 23: 'Barry Grodenchik', 17: 'Rafael Salamanca'}
PAST_COUNCIL_MEMBERS = {1: 'Margaret Chin', 2: 'Rosie Mendez', 3: 'Corey Johnson', 4: 'Daniel Garodnick', 5: 'Ben Kallos', 6: 'Helen Rosenthal', 7: 'Mark Levine', 8: 'Melissa Mark-Viverito', 9: 'Inez Dickens', 10: 'Ydanis Rodriguez', 33: 'Stephen Levin', 34: 'Antonio Reynoso', 35: 'Laurie Cumbo', 36: 'Robert Cornegy', 37: 'Rafael Espinal', 38: 'Carlos Menchaca', 39: 'Brad Lander', 40: 'Mathieu Eugene', 41: 'Darlene Mealy', 42: 'Inez Barron', 43: 'Vincent Gentile', 44: 'David Greenfield', 45: 'Jumaane Williams', 46: 'Alan Maisel', 47: 'Mark Treyger', 48: 'Chaim Deutsch', 19: 'Paul Vallone', 20: 'Peter Koo', 21: 'Julissa Ferreras', 22: 'Costa Constantinides', 23: 'Mark Weprin', 24: 'Rory Lancman', 25: 'Daniel Dromm', 26: 'James Van Bramer', 27: 'Daneek Miller', 28: 'Ruben Wills', 29: 'Karen Koslowitz', 30: 'Elizabeth Crowley', 31: 'Donovan Richards', 32: 'Eric Ulrich', 11: 'Andrew Cohen', 12: 'Andy King', 13: 'James Vacca', 14:'Fernando Cabrera', 15: 'Ritchie Torres', 16: 'Vanessa Gibson', 17: 'Maria del Carmen Arroyo', 18: 'Annabel Palma', 49: 'Deborah Rose', 50: 'Steven Matteo', 51: 'Vincent Ignizio'}

def get_articles(**kwargs):
    """
    returns articles outputted from search
    Necessary inputs for this function:
    show_text, page_range
    Other useful inputs:
    q, fq, begin_date, end_date
    """
    url_start = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=U4XXY5ozk9hpOMIJEAaLAFWPk9Wui5Cl&'
    all_articles = []
    page_range = kwargs['page_range']
    for var_name, val in kwargs.items():
        if var_name != 'page_range' and var_name != 'show_text':
            if var_name == 'fq':
                url_start+=var_name+'='+str(val)+' AND glocations:("NEW YORK CITY")&'
            else:
                url_start += var_name+'='+str(val)+'&'
    for page in range(1, page_range + 1):
        response = requests.get(url_start+'page={}'.format(page))
        if not response.json():
            break
        if organize(response.json(), kwargs['show_text']) is not None:
            all_articles += organize(response.json(), kwargs['show_text'])
    return all_articles

def organize(articles, show_text = True):
    """
    Takes in the result of the NY Times search method (which is a python dictionary)
    Returns: a list of python dictionaries, each dictionary corresponding to an article
            -Contains the following keys:
            'headline', 'date_published', 'url', 'text'
    
    Note: these elements in the dictionary can be changed easily, so please change them if needed.
    I thought these would be nice to have, so change this code if any of this information is useless to have
    """
    if 'response' not in articles.keys():
        return None
    l = []
    for article in articles['response']['docs']:
        new_art = {}
        url=article['web_url']
        new_art['url'] = url
        ##Check to see if article has text:
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            page_soup=soup(webpage,"html.parser")
            content_box=page_soup.find('section', itemprop="articleBody")
            article_text= content_box.text
        except:
            print('There was an error retrieving this text.')
            continue
        new_art['headline'] = article['headline']['main']
        new_art['date_published'] = article['pub_date'][5:7]+'/'+article['pub_date'][8:10]+"/"+article['pub_date'][:4]
        if show_text:
            new_art['text'] = clean_string(article_text)
        l.append(new_art)
    return l

class TestTime(unittest.TestCase):
    def test_time(self):
        articles = get_articles(show_text = True, page_range = 100, q = 'City Council', fq = 'body:("City Council")', begin_date = 20190101, end_date = 20200101)
        for dist, member in CURRENT_COUNCIL_MEMBERS.items():
            articles += get_articles(show_text = True, page_range = 5, fq = 'body:("{}")'.format(member), begin_date = 20190101, end_date = 20200101)
        convert_articles_to_output_file('2019_With_Councilmen.csv', articles)
        self.assertEqual(0,0)

def clean_string(text):
    """
    Helper function that takes in an article text as a string
    Returns: new string with article text cleaned up, punctuation and stop words removed
    """
    useless_words = ['mr.', 'mrs.', 'ms.', 'dr.', 'said', "new yorkers" 'new yorker', 'yorker', 'new york citys', 'new york city', 'city', "new yorks", 'new york', '—']
    text = text.lower()
    punct = '?.,!'
    replacements = {'\n', "'", '"', '”', '’', '“', '‘', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for r in replacements:
        text = text.replace(r, '')
    for word in useless_words:
        text = text.replace(' '+word, '')
        text = text.replace(word+' ', '')
    text = text.replace('  ', ' ')
    return text.strip()

def convert_articles_to_output_file(filename, articles):
    """
    Takes in: a python string for filename, including either '.csv' or '.json' (I can add more filetypes later if needed)
              a list of dictionaries representing articles (the output of the organize function)
    
    Returns: Nothing, this method writes a new file with the given articles and filetype
    """
    if filename[-5:] == '.json':
        with open(filename, 'w') as f:
            json.dump(articles, f)
        print('successfully written '+str(len(articles))+' articles to file: '+filename)
    elif filename[-4:] == '.csv':
        with open(filename, 'w') as f:
            column_names = sorted(articles[0].keys())
            new_f = csv.DictWriter(f, column_names)
            new_f.writeheader()
            new_f.writerows(articles)
        print('successfully written '+str(len(articles))+' articles to file: '+filename)

if __name__ == '__main__':
    all_arts = []
    for dist_num, name in PAST_COUNCIL_MEMBERS.items():
        articles = get_articles(district = dist_num, show_text = True, page_range = 100, fq = 'body:("{}")'.format(name), begin_date = 20130101, end_date = 20170101)
        all_arts += articles
    convert_articles_to_output_file('2013-2016_Council_Articles.csv', all_arts)
