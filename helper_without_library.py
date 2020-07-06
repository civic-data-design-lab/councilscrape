import requests
import json
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup

API_KEY = 'U4XXY5ozk9hpOMIJEAaLAFWPk9Wui5Cl'
'''
url=str(response.json()['response']['docs'][0]['web_url'])
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup=soup(webpage,"html.parser")
content_box=page_soup.find('section', itemprop="articleBody")
content= content_box.text.strip()
'''
def get_articles(api_key, q, fq, page_range = 100, begin_date = None, end_date = None):
    """
    returns articles outputted from search
    """
    all_articles = []
    for page in range(100, page_range+1):
        if begin_date==None and end_date==None:
            response=requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&page={}&api-key={}'.format(q,fq,page,api_key))
        elif begin_date==None and end_date:
            response=requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&page={}&api-key={}&end_date={}'.format(q,fq,page,api_key,end_date))
        elif end_date==None and begin_date:
            response=requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&page={}&api-key={}&begin_date={}'.format(q,fq,page,api_key,begin_date))
        else:
            response=requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&page={}&api-key={}&begin_date={}&end_date={}'.format(q,fq,page,api_key,begin_date,end_date))
        if response.json()['response']['docs']==[]:
            break
        all_articles += organize(response.json(), False)
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
    if articles:
        if 'response' not in articles.keys():
            return None
    l = []
    for article in articles['response']['docs']:
        new_art = {}
        url=article['web_url']
        new_art['url'] = url
        ##Check to see if article has text:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup=soup(webpage,"html.parser")
        try:
            content_box=page_soup.find('section', itemprop="articleBody")
            article_text= content_box.text.strip()
        except:
            continue
        new_art['headline'] = article['headline']['main']
        new_art['date_published'] = article['pub_date'][5:7]+'/'+article['pub_date'][8:10]+"/"+article['pub_date'][:4]
        if show_text:
            new_art['text'] = clean_string(article_text)
        l.append(new_art)
    return l

def clean_string(text):
    """
    Helper function that takes in an article text as a string
    Returns: new string with article text cleaned up
    """
    punct = '?.,!'
    closing = '”’'
    opening = '“‘'
    alph = 'qwertyuiopasdfghjklzxcvbnm'
    '''
    for letter in alph:
        for p in punct:
            text = text.replace(p+letter, p+' '+letter)
            text = text.replace(p+letter.lower(),p + ' '+letter.lower())
    '''
    for c in closing:
        text = text.replace(c, c+' ')
    for o in opening:
        text = text.replace(o, ' '+o)
    replacements = {'\n': '', '‘': "'", '’':"'", "“": '"', "”": '"', '  ': ' '}
    for k, v in replacements.items():
        text = text.replace(k, v)
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
            column_names = articles[0].keys()
            new_f = csv.DictWriter(f, column_names)
            new_f.writeheader()
            new_f.writerows(articles)


if __name__ == '__main__':
    ##Use this to test:
    raw_articles = get_articles(API_KEY, q='City Council', fq = 'body:("Obama")',page_range = 100,begin_date=20120101,end_date=20121231)
    organized = organize(raw_articles, False)
    print(organized)
