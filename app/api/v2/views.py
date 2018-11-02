from flask import jsonify, make_response, Blueprint
from flask_restful import Resource, Api
from app.api.v2.models import ProductsModel, Users, Categories
from app.api.v2.sales import SalesModel


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


class Sales(Resource):
    def __init__(self):
        self.sales = SalesModel()

    def get(self):
        """Get all sales"""
        return self.sales.get_all_sales()

    def post(self):
        """create a new sale"""
        return self.sales.add_sale()


class Sale(Resource):
    """Single sale record functions"""

    def __init__(self):
        self.sales = SalesModel()

    def get(self, sale_id):
        """Get a single sale by sale_id"""
        return self.sales.get_one_sale(sale_id)

    def put(self, sale_id):
        """Update a sale record"""
        return self.sales.update_sale(sale_id)

    def delete(self, sale_id):
        """delete a sale record"""
        return self.sales.delete_sale(sale_id)


class UserLogin(Resource):
    """A user can Login"""

    def __init__(self):
        self.users = Users()

    def post(self):
        return self.users.login()


class UserSignup(Resource):
    """Register a user"""

    def __init__(self):
        self.users = Users()

    def post(self):
        return self.users.add_user()


class UserLogout(Resource):
    """Log out a user"""

    def __init__(self):
        self.users = Users()

    def get(self):
        return self.users.log_out()


class Home(Resource):
    """Home page"""

    def __init__(self):
        pass

    def get(self):
        return make_response(jsonify({"Message": " Welcome to store manager api"}), 200)


class AllUserInformation(Resource):
    """Get registered users"""

    def __init__(self):
        self.users = Users()

    def get(self):
        return self.users.get_all_users()


class SingleUserInformation(Resource):
    """Get and modify user"""

    def __init__(self):
        self.users = Users()

    def get(self, user_id):
        return self.users.get_one_user(user_id)

    def put(self, user_id):
        return self.users.update_user(user_id)


class CategoriesModel(Resource):
    """Create categories and read them"""

    def __init__(self):
        self.category = Categories()

    def post(self):
        """Add a category"""
        return self.category.add_category()

    def get(self):
        """get all categories"""
        return self.category.get_all_categories()


class SingleCategory(Resource):
    """Modify and delete a category"""

    def __init__(self):
        self.category = Categories()

    def put(self, category_id):
        """Update category by id"""
        return self.category.update_category(category_id)

    def delete(self, category_id):
        """delete category"""
        return self.category.delete_category(category_id)


landing_page = Blueprint("landing_page", __name__)
api = Api(landing_page)
api.add_resource(Home, '/', endpoint="landing page")
