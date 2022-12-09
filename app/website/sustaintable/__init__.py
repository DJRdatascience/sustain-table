from pathlib import Path
import pickle
import datetime
import csv
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from . import website_parsers as wp

def _get_ghg( item: str, mass: float ) -> float:
    #lem = lemmatizer.lemmatize( item )
    #name_key = ''#cooks_thesaurus['name_key'][lem] ###### Build
    #return ghg_equivalents[ name_key ] ###### Build
    item = item.lower()
    if item in calculate_co2:
        return calculate_co2[item]*mass
    else:
        return 0.1 * mass

class CustomDict( dict ):
    def __init__(self, factory, dict={}):
        self.factory = factory
        self.missing = []
        self.update(dict)
    def __missing__(self, key):
        self[key] = self.factory(key)
        self._record(key)
        return self[key]
    def _record( self, key ):
        self.missing.append(key)

class Recipe():

    #def __init__( self ):

    def load_from_url( self, url: str ):
        self.url = url
        self.title, self.ingred, self.img_src = wp.scrape( self.url )
        self.mass = [ 1 for i in self.ingred ]
        self.ghg = [ _get_ghg( ingred['name'], mass ) for ingred, mass in zip(self.ingred, self.mass ) ]
        self.ghg_sum = sum( self.ghg ) # This will pass to another .py with carbon calculation
        # self.season # This will calculate when the recipe is in season for a given zipcode

class Repertoire():

    def __init__( self ):
        self.recipes = []
    
    def __len__( self ):
        return len( self.recipes )

    def add_recipe( self, recipe: Recipe ):
        if recipe not in self.recipes:
            self.recipes.append( recipe )

class Account():
    
    def __init__( self, user_name: str, zip_code:int ):
        self.date_created = datetime.datetime.now()
        self.user = user_name
        self.zip = zip_code
        self.repertoire = Repertoire()

class ShoppingList():

    def __init__( self ):
        self.date_created = datetime.datetime.now()
        self.recipes = defaultdict( int )
        self.ingredients = defaultdict( int )
        self.ghg_sum = 0
    
    def __len__ ( self ):
        return len( self.ingredients )

    def add_or_rem_recipe( self, recipe: Recipe, n: int ):
        self.recipes[ recipe ] += n
        self.ghg_sum += n * recipe.ghg_sum
    
    def suggest_substitutions( self ):
        pass
    
    def substitute( self, ingred, ingred_sub ):
        pass

# Load in named ingredients
path = Path(__file__).parent / 'data/named_ingredients.pkl'
with path.open('rb') as f:
    named_ingredients = pickle.load( f )

# Load in Cooks Thesaurus and setup dictionaries
path = Path(__file__).parent / 'data/cooks_thesaurus_dict.pkl'
with path.open('rb') as f:
    cooks_thesaurus = pickle.load( f )
cooks_thesaurus['key'] = CustomDict( lambda x: x, cooks_thesaurus['key'] )
cooks_thesaurus['common'] = CustomDict( lambda x: x, cooks_thesaurus['common'] )
cooks_thesaurus['subs'] = CustomDict( lambda x: [], cooks_thesaurus['subs'] )

# Load in cached word2vec substitutions
path = Path(__file__).parent / 'ml_substitutions.pkl'
with path.open('rb') as f:
    ml_substitutions = pickle.load( f )

def get_subs( ingred: str ) -> list:
    lem = lemmatizer.lemmatize( ingred )
    key = cooks_thesaurus['key'][ lem ]
    # We only use the ml subtitutions if the ingredient is not in the expert model
    if key not in cooks_thesaurus['subs'] and ingred in ml_substitutions:
        return ml_substitutions[ingred]
    else: # This returns the expert subtitutions or, if the ingred is missing, an empty list
        return cooks_thesaurus['subs'][ key ]

# Load in green house gas equivalents
path = Path(__file__).parent / 'data/ghg_equivalents.csv'
calculate_co2 = {
    'diced tomatoes in juice': 1.1,
    'olive oil': 1.63,
    'hot italian sausage': 6.87,
    'small onion': 0.39,
    'arborio rice': 1.14,
    'dry white wine': 1.28,
    'flat-leaf spinach': 0.13,
    'grated parmesan cheese': 9.78,
    'butter': 11.92,
    '': 0
}
with path.open('r') as f:
    reader = csv.reader( f )
    flag = 0
    for row in reader:
        if flag == 0:
            flag = 1
        elif '' not in row[:2]:
            calculate_co2[row[0]] = float(row[1])