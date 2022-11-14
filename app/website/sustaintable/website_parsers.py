import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from parse_ingredients import parse_ingredient as parse_ingred

# Alternate scrapping approach using scrape_me
#from recipe_scrapers import scrape_me
import sys
sys.path.insert(0, '/Users/djr/Documents/python/projects/forks/recipe-scrapers')
from recipe_scrapers import scrape_me


# This is to deal with parse_ingredients printing annoying updates
import contextlib
import sys
class DummyFile(object):
    def write(self, x): pass
@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout

# Parsers for individual web sites
def sk( soup: BeautifulSoup ) -> tuple: #smittenkitchen.com
    title = soup.find( 'h1', {'class': 'entry-title'}  ).text.strip()
    unstruct_ingred = soup.find_all('li', itemprop='recipeIngredient')
    unstruct_ingred = [ i.text.strip() for i in unstruct_ingred ]
    img_src = soup.find( 'div', {'class': 'post-thumbnail-container'} )
    img_src = img_src.img.get('src')
    return title, unstruct_ingred, img_src

# Create beautifulsoup object
def create_soup( url: str ) -> BeautifulSoup:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        request = requests.get( url=url, headers=headers )
        return BeautifulSoup( request.content, features='html.parser' )

# From recipe url, create soup object, get unstructured recipe list and img, parse unstructured recipe
#parsers = { 'smittenkitchen.com': sk } #uncomment to use my own parser
parsers = { }
def scrape( url: str ) -> tuple:
    #
    hostname = urlparse( url ).hostname
    if hostname in parsers:
        soup = create_soup( url )
        title, unstruct_ingred, img_src = parsers[ hostname ]( soup )
    else:
        scraper = scrape_me( url , wild_mode=True )
        title, unstruct_ingred, img_src = scraper.title(), scraper.ingredients(), scraper.image()
    
    struct_ingred = []#[ parse_ingred( i ) for i in unstruct_ingred ] <- implement this when I've made my own parser
    with nostdout():
        for i in unstruct_ingred:
            try:
                struct_ingred.append( parse_ingred( i ).__dict__ )
                if struct_ingred[-1]['name'].lower() == 'sweet or hot italian sausage':
                    struct_ingred[-1]['name'] = 'hot italian sausage'
                    struct_ingred[-1]['quantity'] = 0.75
                if struct_ingred[-1]['name'].lower() in ['dry white wine', 'grated parmesan cheese']:
                    struct_ingred[-1]['quantity'] = 0.5
            except IndexError:
                struct_ingred.append( {
                    'name': '',
                    'quantity': 0,
                    'unit': '',
                    'comment': '',
                    'original_string': i
                } )

    return title, struct_ingred, img_src