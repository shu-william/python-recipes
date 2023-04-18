from flask_app import app
from flask import render_template, redirect, session
from flask_app.models import user, recipe

@app.route('/recipes')
def show_recipes(): # shows recipes with CRUD functionality depending on user
    if 'logged_in' in session:
        data = {
            'id':session['user_id']
        }
        get_user = user.User.get_by_id(data)[0]
        get_recipes = recipe.Recipe.get_all_recipes()
        return render_template("recipes.html", user = get_user, recipes = get_recipes)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')