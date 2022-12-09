from website import create_app
from website.models import IngredProp
from website import db

from website import sustaintable as st

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Initialize with all named ingredients
        ingreds = st.named_ingredients
        ingreds.add('') #empty string for when subs are not found
        for ingred in ingreds:
            new_ingred = IngredProp(
                                    name    = ingred,
                                    img_url = '',
                                    carbon  =  st._get_ghg( ingred, 1 ), #kg CO2 / kg ingred
                                    gluten  = True,
                                    vegan   = True
            )
            db.session.add( new_ingred )
        db.session.commit()