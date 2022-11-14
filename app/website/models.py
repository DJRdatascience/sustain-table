from re import sub
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

##############################################################
# Users
##############################################################

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(150), unique=True)
    password        = db.Column(db.String(150))
    first_name      = db.Column(db.String(150))
    repertoire      = db.relationship('Repertoire')
    grocerylist     = db.relationship('GroceryList')
    mealplan        = db.relationship('MealPlan')

class Repertoire(db.Model):

    __tablename__ = 'Repertoire'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))
    recipe_id       = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    recipe          = db.relationship('Recipe', back_populates='repertoire')

##############################################################
# Recipe data
##############################################################

class Recipe(db.Model): #One row per unique recipe

    __tablename__ = 'Recipe'

    id              = db.Column(db.Integer, primary_key=True)
    #user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))
    name            = db.Column(db.String(10000))
    url             = db.Column(db.String(10000), unique=True)#
    img_url         = db.Column(db.String(10000))
    ghg             = db.Column(db.Float) #total
    repertoire      = db.relationship('Repertoire', back_populates='recipe')
    ingredlist      = db.relationship('IngredList')
    mealplan        = db.relationship('MealPlan')
    
class IngredList(db.Model):

    __tablename__ = 'IngredList'

    id              = db.Column(db.Integer, primary_key=True)
    recipe_id       = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    ingredprop_id   = db.Column(db.Integer, db.ForeignKey('IngredProp.id'))
    quantity        = db.Column(db.String(100))
    unit            = db.Column(db.String(100))
    mass            = db.Column(db.Float)
    

class IngredProp(db.Model):

    __tablename__ = 'IngredProp'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(10000))
    img_url         = db.Column(db.String(10000))
    carbon          = db.Column(db.Float) #kg CO2 / kg ingred
    gluten          = db.Column(db.Boolean)
    vegan           = db.Column(db.Boolean)

##############################################################
# Meal plan
##############################################################

class GroceryList(db.Model):

    __tablename__ = 'GroceryList'

    id              = db.Column(db.Integer, primary_key=True)
    ingred_id       = db.Column(db.Integer, db.ForeignKey('IngredList.id'))
    substitute_id   = db.Column(db.Integer, db.ForeignKey('IngredProp.id'))
    recipe_id       = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))


class MealPlan(db.Model):

    __tablename__ = 'MealPlan'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))
    recipe_id       = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    substitutes     = db.relationship('Substitutes')

class Substitutes(db.Model):

    __tablename__ = 'Substitutes'

    id              = db.Column(db.Integer, primary_key=True)
    mealplan_id     = db.Column(db.Integer, db.ForeignKey('MealPlan.id'))
    grocerylist_id  = db.Column(db.Integer, db.ForeignKey('GroceryList.id'))
    orig            = db.Column(db.Integer, db.ForeignKey('IngredProp.id'))
    sub             = db.Column(db.Integer, db.ForeignKey('IngredProp.id'))
