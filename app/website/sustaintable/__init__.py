import pickle
import datetime
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from . import website_parsers as wp

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


def _get_ghg( item: str, mass: float ) -> float:
    #lem = lemmatizer.lemmatize( item )
    #name_key = ''#cooks_thesaurus['name_key'][lem] ###### Build
    #return ghg_equivalents[ name_key ] ###### Build
    item = item.lower()
    if item in calculate_co2:
        out = calculate_co2[item]*mass
    else:
        out = 0
    return out

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

# Load in Cooks Thesaurus and setup dictionaries
# with open( 'data/cooks_thesaurus.pkl', 'rb' ) as f:
#     cooks_thesaurus = pickle.load( f )
# cooks_thesaurus['name_key'] = CustomDict( function, cooks_thesaurus['name_key'] )
# cooks_thesaurus['common_name'] = CustomDict( function, cooks_thesaurus['common_name'] )
# cooks_thesaurus['substitute'] = CustomDict( function, cooks_thesaurus['substitute'] )

# with open( 'data/ghg_equivalents.pkl', 'rb' ) as f:
#     ghg_equivalents = pickle.load( f )

cooks_thesaurus = defaultdict(lambda:'lemon')
ghg_equivalents = defaultdict(lambda:2)