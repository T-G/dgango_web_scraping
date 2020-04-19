import requests
import re
from requests.utils import requote_uri
# requote_uri adds the %20 instead of a blank space, when user enters the search string in the search field
#from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGLIST_URl = 'https://london.craigslist.org/search/bbb?query={}'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    # store the user input into a variable
    search = request.POST.get('search')
    # insert the search text into the search table in the database
    models.Search.objects.create(search_text=search)
    final_url = BASE_CRAIGLIST_URl.format(requote_uri(search))
    response_from_craiglist_website = requests.get(final_url)
    data = response_from_craiglist_website.text
    # Parsing the beautiful soup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, features='html.parser')
    # Extracting all <a> tags whose class name is 'result-row' into a list
    post_listings = soup.find_all('li', class_='result-row')
    #print('posts: ', post_listings)
    final_postings = []
    for post in post_listings:
        post_title = post.find('a', class_='result-title').text
        post_url = post.find('a', class_='result-title').get('href')
        #post_price = post.find(class_='result-price').text

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))
        #print(final_postings)
        # if post.find(class_='result-price'):
        #     post_price = post.find(class_='result-price').text
        # else:
        #     new_response = request.get(post_url)
        #     new_data = new_response.text
        #     new_soup = BeautifulSoup(new_data, features='html.parser')
        #     post_text = new_soup.find(id='postingbody').text
        #
        #     r1 = re.

    frontend_context = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', frontend_context)