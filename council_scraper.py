import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

district_dict={}
for district in range(1,52):
    url='https://council.nyc.gov/district-{}/'.format(district)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup=soup(webpage,"html.parser")
    content_box=page_soup.find('section')
    content= content_box.text.strip()
    district_dict[district]=content


