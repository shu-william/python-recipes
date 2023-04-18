from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("logreg.html")

@app.route('/register', methods=['POST'])
def process_register():
    session.clear()
    data = {}
    for item in request.form:
        if item == 'password' or item == 'conf_password':
            continue
        data[item] = request.form[item]
        session[item] = request.form[item]
    if not user.User.validate_registration(request.form):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    user_id = user.User.save(data)
    session['logged_in'] = True
    session['user_id'] = user_id
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def process_login():
    session['login_email'] = request.form['email']
    if not user.User.validate_login(request.form):
        return redirect('/')
    data = {
        'email' : request.form['email']
    }
    get_user = user.User.get_by_email(data)[0]
    if not bcrypt.check_password_hash(get_user['password'], request.form['password']):
        flash("Password is incorrect.", "login")
        return redirect('/')
    session['logged_in'] = True
    session['user_id'] = get_user['id']
    return redirect('/recipes')