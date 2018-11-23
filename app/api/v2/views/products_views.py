from flask_restful import Resource
from app.api.v2.models.products_model import ProductsModel


class Products(Resource):
    """get all Products or post a product to the products list"""

    def __init__(self):
        self.product = ProductsModel()

    def get(self):
        """get all Products from products list"""
        return self.product.get_all_products()

    def post(self):
        """Add a product to the products list"""
        return self.product.add_product()


class Product(Resource):
    """get or update or delete a single product from the products list """

    def __init__(self):
        self.product = ProductsModel()

    def get(self, product_id):
        """get a single product from the products list """
        return self.product.get_one_product(product_id)

    def put(self, product_id):
        """update a single product from the products list """
        return self.product.update_product(product_id)

    def delete(self, product_id):
        """delete a single product from the products list """
        return self.product.delete_product(product_id)