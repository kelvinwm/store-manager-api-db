from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from app.api.v2.models import Products, Users

product = Products()
users = Users()


class Products(Resource):
    """get all Products or post a product to the products list"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("product_name", required=True, help="Invalid entry", location=['json'])
        self.parser.add_argument("price", required=True, type=int, help="Invalid entry", location=['json'])
        self.parser.add_argument("description", required=True, help="Invalid entry", location=['json'])
        self.parser.add_argument("quantity", required=True, type=int, help="Invalid entry", location=['json'])
        super().__init__()

    def get(self):
        """get all Products from products list"""
        return product.get_all_products()

    def post(self):
        """Add a product to the products list"""
        args = self.parser.parse_args()
        return product.add_product(**args)


class Product(Resource):
    """get or update or delete a single product from the products list """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("product_name", required=True, help="Invalid entry", location=['json'])
        self.parser.add_argument("price", required=True, type=int, help="Invalid entry", location=['json'])
        self.parser.add_argument("description", required=True, help="Invalid entry", location=['json'])
        self.parser.add_argument("quantity", required=True, type=int, help="Invalid entry", location=['json'])
        super().__init__()

    def get(self, product_id):
        """get a single product from the products list """
        return product.get_one_product(product_id)

    def put(self, product_id):
        """update a single product from the products list """
        args = self.parser.parse_args()
        return product.update_product(product_id, **args)

    def delete(self, product_id):
        """delete a single product from the products list """
        return product.delete_product(product_id)


class UserLogin(Resource):
    def post(self):
        return users.login()


class UserSignup(Resource):
    def post(self):
        return users.add_user()


class Home(Resource):
    def get(self):
        return make_response(jsonify({"Message": " Welcome to store manager api"}), 200)
