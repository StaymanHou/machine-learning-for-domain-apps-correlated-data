import requests
from bs4 import BeautifulSoup
import json

cats = [
    'Adult',
    'Arts',
    'Business',
    'Computers',
    'Games',
    'Health',
    'Home',
    'Kids_and_Teens',
    'News',
    'Recreation',
    'Reference',
    'Regional',
    'Science',
    'Shopping',
    'Society',
    'Sports',
]

pages = range(20)

data = []

for cat in cats:
    print('fetching cat: '+cat)
    for page in pages:
        print('page: #'+str(page))
        url = 'http://www.alexa.com/topsites/category;'+str(page)+'/Top/'+cat
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html)
        site_listing_elements = soup.find_all('li', class_='site-listing')
        for e in site_listing_elements:
            domain = e.a.text.lower()
            datum = [domain, cat]
            data.append(datum)

json_str = json.dumps(data)
f = open('alexa.json', 'w')
f.write(json_str)
