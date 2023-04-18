from flask_app import app
from flask_app.controllers import log_reg_routes, recipe_routes, user_routes

if __name__=="__main__":
    app.run(debug=True)