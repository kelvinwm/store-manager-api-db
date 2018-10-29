from flask import jsonify, make_response, Blueprint
from flask_restful import Resource, reqparse, Api
from app.api.v2.models import Products, Users, Categories

product = Products()
users = Users()
category = Categories()


class Products(Resource):
    """get all Products or post a product to the products list"""
    def get(self):
        """get all Products from products list"""
        return product.get_all_products()

    def post(self):
        """Add a product to the products list"""
        return product.add_product()


class Product(Resource):
    """get or update or delete a single product from the products list """

    def get(self, product_id):
        """get a single product from the products list """
        return product.get_one_product(product_id)

    def put(self, product_id):
        """update a single product from the products list """
        return product.update_product(product_id)

    def delete(self, product_id):
        """delete a single product from the products list """
        return product.delete_product(product_id)


class UserLogin(Resource):
    """A user can Login"""
    def post(self):
        return users.login()


class UserSignup(Resource):
    """Register a user"""
    def post(self):
        return Users().add_user()


class UserLogout(Resource):
    """Log out a user"""
    def get(self):
        return users.log_out()


class Home(Resource):
    """Home page"""
    def get(self):
        return make_response(jsonify({"Message": " Welcome to store manager api"}), 200)


class AllUserInformation(Resource):
    """Get registered users"""
    def get(self):
        return users.get_all_users()


class SingleUserInformation(Resource):
    """Get and modify user"""
    def get(self, user_id):
        return users.get_one_user(user_id)

    def put(self, user_id):
        return users.update_user(user_id)


class Categories(Resource):
    """Create categories and read them"""
    def post(self):
        return category.add_category()

    def get(self):
        return category.get_all_categories()


class SingleCategory(Resource):
    """Modify and delete a category"""
    def put(self, category_id):
        return category.update_category(category_id)

    def delete(self, category_id):
        return category.delete_category(category_id)


landing_page = Blueprint("landing_page", __name__)
api = Api(landing_page)
api.add_resource(Home, '/', endpoint="landing page")
