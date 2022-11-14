import unittest
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, user_unauthorized
from .models import User, Repertoire, Recipe, IngredList, IngredProp, GroceryList, MealPlan, Substitutes
from . import db
import json
import requests
from . import sustaintable as st
from sqlalchemy.orm import aliased



import sys
sys.path.insert(0, '/Users/djr/Documents/python/projects/forks/recipe-scrapers')
import recipe_scrapers

banned_names = ['pasta water','water']

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        recipe_url = request.form.get('Recipe')
        recipe = db.session.query(Recipe).filter_by(url=recipe_url).first()
        if recipe is None:
            try:
                # RECIPE
                new_recipe = st.Recipe()
                new_recipe.load_from_url( recipe_url )
                recipe =  Recipe(   name = new_recipe.title,
                                    url = new_recipe.url,
                                    img_url = new_recipe.img_src,
                                    ghg = new_recipe.ghg_sum
                )
                db.session.add( recipe )
                db.session.flush()

                # INGREDIENTS
                ingred_list = []
                for ingred, mass, carbon in zip(new_recipe.ingred, new_recipe.mass, new_recipe.ghg):
                    if ingred['name'] and ingred['name'] not in banned_names:
                        # if ingred['name'].lower() == 'sweet or hot italian sausage':
                        #     ingred['name'] = 'hot italian sausage'
                        ingred_id = db.session.query(IngredProp.id).filter_by(name=ingred['name']).first()
                        if ingred_id is None:
                            new_ingred = IngredProp(    name            = ingred['name'],
                                                        img_url         = 'www',
                                                        carbon          = carbon,
                                                        gluten          = False,
                                                        vegan           = False,
                            )
                            db.session.add( new_ingred )
                            db.session.flush()
                        ingred_id = db.session.query(IngredProp.id).filter_by(name=ingred['name']).first()[0]
                        ingred_list.append( IngredList( recipe_id       = recipe.id,
                                                        quantity        = ingred['quantity'],
                                                        unit            = ingred['unit'],
                                                        mass            = mass,
                                                        ingredprop_id   = ingred_id
                        ))
                db.session.add_all( ingred_list )

            except recipe_scrapers._exceptions.NoSchemaFoundInWildMode:
                flash('Recipe retrieval failed (no schema found).', category='error')
            except:
                flash('Recipe retrieval failed.', category='error')
        
        if recipe is not None:
            in_db = db.session.query(Repertoire).filter_by(user_id=current_user.id,recipe_id=recipe.id).first()
            if in_db is None:
                rep = Repertoire(   user_id     = current_user.id,
                                    recipe_id   = recipe.id
                )
                db.session.add(rep)
                flash('Recipe added.', category='success')
            else:
                flash('Recipe already in repertoire.', category='error')
            db.session.commit()
        
    return render_template("home.html", user=current_user)


@views.route('/repertoire', methods=['GET', 'POST'])
@login_required
def repertoire():
    return render_template("repertoire.html", user=current_user) #, 

@views.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    sub = False
    SubProp = aliased( IngredProp )
    meals = (GroceryList.query.filter(GroceryList.user_id == current_user.id)
                        .join(Recipe, GroceryList.recipe_id == Recipe.id)
                        .add_columns( Recipe.ghg )
    )
    ghg = 0
    for meal in meals.all()[-1:]:
        ghg += meal.ghg
        print('1')
    carbon = [ghg,ghg]
    groceries = (   GroceryList.query
                                .filter( GroceryList.user_id == current_user.id )
                                .join(IngredList, GroceryList.ingred_id==IngredList.id)
                                .add_columns( GroceryList.id, IngredList.ingredprop_id, IngredList.quantity, IngredList.unit)
                                .join(IngredProp, IngredList.ingredprop_id==IngredProp.id)
                                .add_columns(IngredProp.name, IngredProp.carbon)
                                .join(SubProp, GroceryList.substitute_id==SubProp.id)
                                .add_columns(SubProp.name.label('substitute_name'),SubProp.id.label('substitute_id'), SubProp.carbon.label('substitute_carbon'))
    )
    if request.method == 'POST':
        if request.form.get('cl_button') == 'sub_init':
            sub = True
        elif request.form.get('sub_button') is not None:
            sub = True
            gl_id = int( request.form.get('sub_button') )
            in_sub = db.session.query(Substitutes).filter_by(grocerylist_id=gl_id)
            if not in_sub.first():
                mealplan_id = db.session.query(MealPlan.user_id).filter_by(user_id=current_user.id).first()[0]
                gl_orig = db.session.query(GroceryList.ingred_id).filter_by(id=gl_id).first()[0]
                gl_sub = db.session.query(GroceryList.substitute_id).filter_by(id=gl_id).first()[0]
                new_sub = Substitutes(  mealplan_id     = mealplan_id,
                                        grocerylist_id  = gl_id,
                                        orig            = gl_orig,
                                        sub             = gl_sub
                                )
                db.session.add( new_sub )
                carbon[1] = round(carbon[1]-6.87+0.9,2)
            else:
                in_sub.delete()
                carbon[1] = carbon[0]
            
            db.session.commit()

    substitutes = Substitutes.query.add_columns(Substitutes.grocerylist_id).all()
    substitutes = [r[1] for r in substitutes]
    return render_template("list.html", user=current_user, groceries=groceries, sub=sub, substitutes=substitutes, carbon=carbon ) #, 


@views.route('/delete-recipe', methods=['POST'])
def delete_recipe():
    recipe = json.loads(request.data)
    recipe_id = recipe['recipeId']
    recipe = Repertoire.query.get(recipe_id)
    print(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted.', category='success')
    return jsonify({})

@views.route('/add-recipe', methods=['POST'])
def add_recipe():
    recipe = json.loads(request.data)
    recipe_id = recipe['recipeId']
    recipe = Repertoire.query.get(recipe_id)
    ingredients = db.session.query(IngredList).filter_by(recipe_id=recipe.id).all()
    if ingredients:
        shopping_list = []
        for ingred in ingredients:
            ip = db.session.query(IngredProp.name).filter_by(id=ingred.ingredprop_id).first()[0]
            if ip == 'hot italian sausage':
                substitute = 2
            else:
                substitute = 1
            sl =  GroceryList(  ingred_id       = ingred.id,
                                substitute_id   = substitute,
                                recipe_id       = recipe.id,
                                user_id         = current_user.id
            )
            shopping_list.append(sl)
        mp = MealPlan(  user_id     = current_user.id,
                        recipe_id   = recipe.id
        )
        db.session.add_all( shopping_list+[mp] )
        db.session.commit()
        flash('Recipe added to shopping list.', category='success')
    return jsonify({})