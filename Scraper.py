
# coding: utf-8

# In[10]:


import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from warnings import warn
from IPython.core.display import clear_output
from time import time

# The number of pages and number of years to scrape
pages = [str(i) for i in range(1,8000,51)]
years_url = [str(i) for i in range(2017,2019)]
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Lists to store scraped data 
names = [] 
years = []
imdb_ratings = []
metascores = []
votes = []
genres = []

# Tracking the number of requests to IMDb
start_time = time()
requests = 0

# For every year in the years interval
for year_url in years_url:
    
    # For every page in the page interval
    for page in pages:
        
        # Make a get request to IMDb
        response = get('http://www.imdb.com/search/title?title_type=feature&release_date=' + year_url + 
        '&sort=num_votes,desc&start=' + page + '&ref_=adv_nxt', headers = headers)
        
        # Pause the loop
        sleep(randint(8,15))
        
        # Monitor the requests and printing 
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)
        
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
        
        # Break the loop if the number of requests is greater than 72 pages
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:

            # Include only if movie has a Metascore - future titles do not
            if container.find('div', class_ = 'ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year 
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                # Scrape the IMDb rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))

                # Scrape the number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))
                
                # Scrape the genre
                genre = container.find('span', class_ = 'genre').text
                genres.append(genre.strip())

test_df = pd.DataFrame({'movie':names,
'year':years,'imdb':imdb_ratings,'genre':genres,'votes':votes,
'metascore':metascores})

print(test_df.info())
test_df.head(200)
test_df.to_csv('IMDbExport.csv', sep=',')

