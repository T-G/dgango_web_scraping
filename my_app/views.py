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

        # check if data-ids is present in the result-image
        if post.find(class_='result-image').get('data-ids'):
            CRAIGLIST_IMAGES_URL = 'https://images.craigslist.org/{}'
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = CRAIGLIST_IMAGES_URL.format(post_image_id) + '_600x450.jpg'
            #print(post_image_url)
        else:
            post_image_url = 'https://london.craigslist.org/images/peace.jpg'


        final_postings.append((post_title, post_url, post_price, post_image_url))
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