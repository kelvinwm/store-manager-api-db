from flask_restful import Resource

from app.api.v2.models.sales_model import SalesModel


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