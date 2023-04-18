from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

DB = 'recipes_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users 
        (first_name, last_name, email, password) 
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;""" 
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_emails(cls):
        query = "SELECT email FROM users;"
        results = connectToMySQL(DB).query_db(query)
        emails = []
        for email in results:
            emails.append(email['email'])
        return emails

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_with_recipes(cls, data):
        query = """SELECT * FROM users
        LEFT JOIN recipes
        ON recipes.user_id = users.id
        WHERE users.id = %(id)s
        ;"""
        results = connectToMySQL(DB).query_db(query, data)
        user = cls(results[0])
        for row in results:
            recipe_data = {
                'id' : row['recipes.id'],
                'name' : row['name'],
                'description' : row['description'],
                'instructions' : row['instructions'],
                'date_cooked' : row['date_cooked'],
                'under_30' : row['under_30'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            user.recipes.append(recipe.Recipe(recipe_data))
        return user


    @staticmethod
    def validate_registration(user):
        is_valid = True
        if not NAME_REGEX.match(user['first_name']) or len(user['first_name']) < 2:
            flash("First name must have at least 2 letters, A-Z only.", "register")
            is_valid = False
        if not NAME_REGEX.match(user['last_name']) or len(user['last_name']) < 2:
            flash("Last name must have at least 2 letters, A-Z only.", "register")
            is_valid = False
        if user['email'] in User.get_emails():
            flash("Email is already in use.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            if len(user['email']) < 1:
                flash("Email is required.", "register")
                is_valid = False
            else:
                flash("Invalid email address.", "register")
                is_valid = False
        if not PASS_REGEX.match(user['password']) or len(user['password']) < 8:
            flash("Password must be at least 8 characters and must contain one uppercase letter, one lowercase letter, and one number.", "register")
            is_valid = False
        if user['password'] != user['conf_password']:
            flash("Passwords must match.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if user['email'] not in User.get_emails():
            flash("We could not find the associated email in our user database.", "login")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password is required.")
            is_valid = False
        return is_valid