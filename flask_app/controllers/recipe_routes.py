from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe

@app.route('/recipes/new')
def create_recipe():
    if 'logged_in' in session:
        data = {
            'id':session['user_id']
        }
        get_user = user.User.get_by_id(data)[0]
        return render_template("new_recipe.html", user = get_user)
    return redirect('/')

@app.route('/process_new_recipe', methods=['POST'])
def process_new_recipe():
    data = {}
    for item in request.form:
        data[item] = request.form[item]
        session[item] = request.form[item]
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe.Recipe.save(data)
    session.pop('name', None)
    session.pop('description', None)
    session.pop('instructions', None)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'logged_in' in session:
        data = {
            'id': session['user_id'],
            'recipe_id': id
        }
        get_user = user.User.get_by_id(data)[0]
        this_recipe = recipe.Recipe.get_by_id(data)
        return render_template("show_recipe.html", recipe = this_recipe, user = get_user)
    return redirect('/logout')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'logged_in' in session:
        data = {
            'id': session['user_id'],
            'recipe_id': id
        }
        this_recipe = recipe.Recipe.get_by_id(data)
        if this_recipe.users_id == data['id']: # checks to make sure the editor is the creator of the recipe
            return render_template("edit_recipe.html", recipe = this_recipe)
    return redirect('/logout')

@app.route('/process_edit_recipe', methods=['POST'])
def process_edit_recipe():
    data = {}
    for item in request.form:
        data[item] = request.form[item]
        session[item] = request.form[item]
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit/' + data['id'])
    recipe.Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'logged_in' in session:
        data = {
            'id': session['user_id'],
            'recipe_id': id
        }
        this_recipe = recipe.Recipe.get_by_id(data)
        if this_recipe.users_id == data['id']: # checks to make sure the editor is the creator of the recipe
            recipe.Recipe.delete(data)
            return redirect('/recipes')
    return redirect('/logout')