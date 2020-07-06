import requests
import json
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import unittest

TEST_STRING2 = ''
TEST_STRING = 'If you are a New Yorker and sort your recycling at home, as city law mandates, you probably wonder, as you rinse bottles and stack junk mail and scrub yogurt containers: Does all this effort make a difference?Well, yes, but not nearly as much as it could. New York City recycles only about a fifth of its garbage — 18 percent of trash from homes and about 25 percent from businesses — according to the city’s Department of Sanitation.Yet seven years ago, Mayor Michael R. Bloomberg vowed to double the residential recycling rate to 30 percent by 2017.The numbers fall far short of New York’s potential. If everything recyclable were sorted and recycled, some 68 percent of residential trash and 75 percent of commercial trash could be kept out of landfills, according to the Sanitation Department. And while city leaders have sought to improve recycling for decades, New York still lags behind major cities like Seattle and San Francisco, which recycle more than half of their waste — numbers attained over decades of policies that include stronger requirements than New York’s.The cascading effects of not recycling enough — such as clogged trash chutes in public housing, garbage that must be trucked out of the city, and organic waste left to decompose and spew planet-warming methane gas — ultimately undermine ambitious targets the city and state enshrined in law last year to radically reduce contributions to climate change.“This is the year New York has to get serious about solving the solid waste crisis,” said Peter Iwanowicz, executive director of Environmental Advocates of New York. “Otherwise it’s going to impact our ability to hit our climate goals.”How, though, does a city that promotes itself as a leader on the environment and climate change — and where a zero-waste campaign aims to stop exports of garbage to faraway landfills by 2030 — stumble on recycling? Here are seven of the reasons.♳ The city’s composting plan is behind scheduleAbout a third of residential waste is made up of food scraps and yard rubbish — organic materials that can be composted and turned into fertilizers or biogas, which can be used to produce energy. The city’s sanitation commissioner, Kathryn Garcia, has been a proponent of composting as a way to reduce waste.But a composting program that the Bloomberg administration began in 2013 appears to have stalled, according to Politico, whose recent investigation of New York’s recycling program concluded that the city is not meeting the recycling goals set by the de Blasio and Bloomberg administrations.Mayor Bill de Blasio had vowed in his first term to make the composting program citywide by 2018, but has since put funding on hold.Many neighborhoods do not even have the option to get city composting bins, and only the largest restaurants are required to separate food scraps.A big reason for the problem, experts say, is money. Recycling paper and glass can be profitable for the city, depending on markets, but so far composting costs far more than it can earn.♴ Most public housing units lack conveniently placed recycling binsSeparating garbage became required for residents in 1989. But by 2015, just 15 percent of New York City Housing Authority complexes had recycling bins, according to Politico.Public housing residents in the Brownsville section of Brooklyn threatened a lawsuit against the city that year for failing to provide recycling bins, and the city promised to put some outside all complexes within a year. But many apartments are a long walk from those bins — which in privately owned buildings are usually located on each floor — and New York’s nearly 400,000 public housing residents recycle less than 2 percent of their household waste.Recyclables swell the regular garbage, contributing to overflowing trash cans and chutes.These residents, of course, are not the only New Yorkers eschewing recycling. And when people do recycle, they are not always following the rules: Bins often include containers smeared with food, or items that are not recyclable.♵ Politicians are wary of requiring more recyclingCities with better recycling rates tend to have tougher mandates and enforcement than in New York. In some European cities, for instance, residents must pay for every bag of trash and recyclables collected, providing incentives not just to sort garbage, but to buy less and reuse more.In Seattle, recycling is collected for free, but residents pay a fee for each bag of regular garbage. People who support such systems, called “pay as you throw” or “save as you throw,” say that without fees, garbage collection is an “unmetered utility,” akin to receiving unlimited water or electricity for free.But in New York, Corey Johnson, the City Council speaker, has called such a requirement a “nonstarter.” For now, fines for failing to recycle are charged to property owners — a weak measure when most New Yorkers rent their homes. In any case, the fine charged to landlords is $25 per violation, and recycling advocates say inspections are inadequate.♶ Businesses sort recycling, but garbage crews mix it back inOn a recent ride with a garbage workers’ union official, who tailed the privately owned trucks that pick up trash from businesses, I saw several crews take sorted garbage from outside businesses — tied stacks of cardboard, bags of cans and bottles — and dump it into the maws of their trucks with regular garbage.Overworked crews are under pressure to complete long pickup routes, said Sean T. Campbell, the Teamsters local president who had been driving me around Brooklyn. The workers know, he said, that many of the lightly regulated transfer stations where they take recyclables often remix them with garbage anyway.Private trash companies say such violations are isolated incidents.A new law to reshape commercial collection is designed to stop such practices, but will not take full effect for several years. And it could take longer to undo the impression made on restaurant workers and office tenants who know about the remixing, said Michael B. Gerrard, director of the Sabin Center for Climate Change Law at Columbia University.“They become discouraged and stop bothering to separate their garbage in the first place,” Mr. Gerrard said.♷ Markets are bearish on recycled materialsChina, in recent years, has tightened its standards for buying recycled materials, creating a disincentive for waste collectors to sort paper and cardboard.According to Ms. Garcia, the sanitation commissioner, New York has been relatively insulated from the market swings because half of its residential paper and cardboard waste goes to a paper mill on Staten Island. The mill recycles the materials locally, making the city less dependent on selling them overseas.But Mr. Campbell, the Teamsters president, said commercial garbage collectors are less likely to separate cardboard from trash when the market is low.“When the market is high,” he said, “you’ll see scavengers driving around in pickup trucks, picking up cardboard to sell. By the time the garbage trucks come, it’s gone.”♸ Recycling bulky construction debris is not requiredAbout half of construction debris is recycled, according to self-reporting by private transfer stations, the mini-dumps where the waste is moved to larger trucks and shipped out of town.But the real number may be lower, especially since some waste is trucked directly out of the city without stopping at a transfer station.♹ New Yorkers love consumerism and convenienceA discussion of recycling would be incomplete without acknowledging that many New Yorkers consider the ability to have pretty much anything delivered, within days if not hours, to be a virtual right, and part of the city’s identity. That means more takeout containers and cardboard boxes.“It’s New York,” Ms. Garcia said. “People don’t have cars, and they like to order stuff. Now, with the Amazon effect, people don’t just order big boxes. They order one bottle of detergent.”'
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
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup=soup(webpage,"html.parser")
        try:
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
    punct = '?.,!'
    closing = '”’'
    opening = '“‘'
    alph = 'qwertyuiopasdfghjklzxcvbnm'
    # for letter in alph:
    #     for p in punct:
    #         text = text.replace(p+letter, p+' '+letter)
    #         text = text.replace(p+letter.lower(),p + ' '+letter.lower())
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
