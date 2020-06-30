import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

response=requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&fq=body:("Obama")&api-key=KxkgQ4Rigb0c3KRjiGFDfL85PwA29ktb')
#print(response.json()['response']['docs'][0].keys())
url=str(response.json()['response']['docs'][0]['web_url'])
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup=soup(webpage,"html.parser")
content_box=page_soup.find('section', itemprop="articleBody")
content= content_box.text.strip()
print(content)

