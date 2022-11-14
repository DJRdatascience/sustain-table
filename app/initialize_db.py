from website import create_app
from website.models import IngredProp
from website import db

app = create_app()

with app.app_context():
    # Initialize
    new_ingred = IngredProp(
                            name    = '',
                            img_url = 'www',
                            carbon  =  0, #kg CO2 / kg ingred
                            gluten  = False,
                            vegan   = False
    )
    db.session.add( new_ingred )
    new_ingred = IngredProp(
                            name    = 'beyond/impossible sausage',
                            img_url = 'www',
                            carbon  =  0.9, #kg CO2 / kg ingred
                            gluten  = True,
                            vegan   = True
    )
    db.session.add( new_ingred )
    db.session.commit()