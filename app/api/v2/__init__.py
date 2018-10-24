from flask import Blueprint
from flask_restful import Api
from app.api.v2.views import (Products, Product, Home, UserSignup, UserLogin)

version_2 = Blueprint("version_2", __name__)
api = Api(version_2)
api.add_resource(Products, '/products', endpoint="products")
api.add_resource(Product, '/products/<int:product_id>', endpoint="product")
api.add_resource(Home, '/', endpoint="Home")
api.add_resource(UserSignup, '/auth/signup', endpoint="auth_signup")
api.add_resource(UserLogin, '/auth/login', endpoint="auth_login")