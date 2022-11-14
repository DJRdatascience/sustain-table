from website import create_app
from website.models import IngredProp
from website import db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Initialize - placeholder for now
        new_ingred = IngredProp(
                                name    = 'beyond/impossible sausage',
                                img_url = 'www',
                                carbon  =  0.9, #kg CO2 / kg ingred
                                gluten  = True,
                                vegan   = True
        )
        db.session.add( new_ingred )
        db.session.commit()