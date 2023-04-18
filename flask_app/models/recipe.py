from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import datetime, math

DB = 'recipes_db'

class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes
        (name, description, instructions, date_cooked, under_30, users_id)
        VALUES
        (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(users_id)s)
        ;"""
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.users_id
        WHERE recipes.id = %(recipe_id)s
        ;"""
        results = connectToMySQL(DB).query_db(query, data)
        all_data = results[0]
        recipe_data = cls(all_data)
        user_data = {
                "id": all_data['users.id'],
                "first_name": all_data['first_name'],
                "last_name": all_data['last_name'],
                "email": all_data['email'],
                "password": "",
                "created_at": all_data['users.created_at'],
                "updated_at": all_data['users.updated_at']
            }
        recipe_data.creator = user.User(user_data)
        return recipe_data

    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.users_id
        ;"""
        results = connectToMySQL(DB).query_db(query)
        recipe_list = []
        for row in results:
            recipe_data = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            recipe_data.creator = user.User(user_data)
            recipe_list.append(recipe_data)
        return recipe_list

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_30 = %(under_30)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Recipe name must contain at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must contain at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must contain at least 3 characters.", "recipe")
            is_valid = False
        try:
            datetime.datetime.strptime(recipe['date_cooked'], '%Y-%m-%d')
        except ValueError:    
            flash("Please select a valid date.", "recipe")
            is_valid = False
        if 'under_30' not in recipe:
            flash("Please specify whether the recipe can be made within 30 minutes.", "recipe")
            is_valid = False
        return is_valid
