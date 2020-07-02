import requests
import json
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
from nytimesarticle import articleAPI

API_KEY = 'U4XXY5ozk9hpOMIJEAaLAFWPk9Wui5Cl'

def get_articles(**kwargs):
    """
    Uses nytimesarticle library to search nytimes API
    """
    api = articleAPI(API_KEY)
    return api.search(**kwargs)
     
def get_text_from_url(url_link):
    """
    Takes a url as input (as a standard python str)

    Returns: Body text from given url as a standard python string
    Some text includes line skips (\n)'s.
    """
    ##get url request
    r = Request(url_link, headers = {'User-Agent': 'Mozilla/5.0'})
    ##get webpage
    try:
        page = bs(urlopen(r).read(), 'html.parser')
    except HTTPError: ##raised if url page no longer exists
        return None
    content_body = page.find('section', itemprop='articleBody')
    try:
        content_text = content_body.text.strip()
    except AttributeError:
        return None
    return content_text

def organize(articles, show_text = True):
    """
    Takes in the result of the NY Times search method (which is a python dictionary)

    Returns: a list of python dictionaries, each dictionary corresponding to anm article
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
        new_art['url'] = article['web_url']
        ##Check to see if article has text:
        article_text = get_text_from_url(article['web_url'])
        if article_text is None: ##ignore the article if no text inside
            continue
        new_art['headline'] = article['headline']['main']
        new_art['date_published'] = article['pub_date'][5:7]+'/'+article['pub_date'][8:10]+"/"+article['pub_date'][:4]
        if show_text:
            new_art['text'] = get_text_from_url(article['web_url'])
        l.append(new_art)
    return l

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
            column_names = articles[0].keys()
            new_f = csv.DictWriter(f, column_names)
            new_f.writeheader()
            new_f.writerows(articles)


if __name__ == '__main__':
    ##Use this to test:
    raw_articles = get_articles(q='City Council', fq = {}, begin_date = 20200101)
    organized = organize(raw_articles, False)
    print(organized)
  
