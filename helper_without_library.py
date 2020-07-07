import requests
import json
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import unittest

API_KEY = 'U4XXY5ozk9hpOMIJEAaLAFWPk9Wui5Cl'

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
            continue
        new_art['headline'] = article['headline']['main']
        new_art['date_published'] = article['pub_date'][5:7]+'/'+article['pub_date'][8:10]+"/"+article['pub_date'][:4]
        if show_text:
            new_art['text'] = clean_string(article_text)
        l.append(new_art)
    return l

class TestTime(unittest.TestCase):
    def test_time(self):
        articles = get_articles(show_text = True, page_range = 1, q = 'City Council', fq = 'body:("City Council")', begin_date = 20200101)
        self.assertEqual(0,0)

def clean_string(text):
    """
    Helper function that takes in an article text as a string

    Returns: new string with article text cleaned up
    """
    punct = ['"', "'", '’','‘', '“', '”', '?', ',', '!', '\n', '.', ';']
    for p in punct:
        text = text.replace(p, '')
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
    elif filename[-4:] == '.csv':
        with open(filename, 'w') as f:
            column_names = sorted(articles[0].keys())
            new_f = csv.DictWriter(f, column_names)
            new_f.writeheader()
            new_f.writerows(articles)

if __name__ == '__main__':
    ##Use this to test:
    # raw_articles = get_articles(API_KEY, q='City Council', fq = 'body:("City Council")',begin_date=20200101,end_date=20200201)
    # organized = organize(raw_articles)
    # for a in organized:
    #     pass
    # text = organized[2]['text']
    # t = timeit.timeit(""""clean_string(text)""")  
    # print(t)
    # with open('starwarstest.txt', 'r') as f:
    #     for line in f:
    #         TEST_STRING2+=line
    # res = unittest.main(verbosity=3, exit=False)
    # articles = get_articles(show_text = False, page_range = 1, q = 'City Council', fq = 'body:("City Council")', begin_date = 20200101)
    # print(articles, len(articles))
    pass
