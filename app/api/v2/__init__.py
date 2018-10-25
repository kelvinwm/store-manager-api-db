from flask import Blueprint
from flask_restful import Api
from app.api.v2.views import (Products, Product, Home, UserSignup, UserLogin, UserLogout,
                              AllUserInformation, SingleUserInformation, Categories, SingleCategory)

version_2 = Blueprint("version_2", __name__)
api = Api(version_2)
api.add_resource(Products, '/products', endpoint="products")
api.add_resource(Product, '/products/<int:product_id>', endpoint="product")
api.add_resource(Home, '/', endpoint="Home")
api.add_resource(UserSignup, '/auth/signup', endpoint="auth_signup")
api.add_resource(UserLogin, '/auth/login', endpoint="auth_login")
api.add_resource(UserLogout, '/auth/logout', endpoint="auth_logout")
api.add_resource(AllUserInformation, '/users', endpoint="users")
api.add_resource(SingleUserInformation, '/users/<int:user_id>', endpoint="user")
api.add_resource(Categories, '/category', endpoint="categories")
api.add_resource(SingleCategory, '/category/<int:category_id>', endpoint="category")
