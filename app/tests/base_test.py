import json
import unittest
from db_init import drop_tables

from app import create_app


class BaseTest(unittest.TestCase):
    """TEST CLASS FOR AUTHENTICATION API ENDPOINTS"""

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.sign_up_data = {"first_name": "KLEVIN", "last_name": "WMUINDE", "email": "kevmwk@gmail.com",
                             "password": "25s#sssA4"}
        self.login_data = {"email": "peterkelvin@storemanager.com", "password": "25s#sssA4"}
        self.invalid_sign_up_data = {"first_name": "BEN10", "last_name": "THE4TH", "email": "ben10storemanager.com",
                                     "password": "25s#sssA4"}
        self.empty_login_data = {"email": "", "password": ""}
        self.invalid_login_data = {"username": "kevo", "email": "prince@gmail.com", "password": "12ds9vs33"}
        self.result = self.app.post('/api/v2/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoidHJ1ZSIsInVzZXJuYW1lIjoicGV0ZXJrZWx2aW5Ac" \
                     "3RvcmVtYW5hZ2VyLmNvbSIsImV4cCI6MTU0NjkyMDk4MX0.LV-n4s9z4DBSEzFM7WrIAGVkFGat8reEBxQppUo3H3s"
        self.headers = {'content-type': 'application/json', 'access-token': self.token}
        self.category = {"category": "klb"}
        self.category_update = {"category": "klb"}
        self.add_product = {"category": "KLB", "price": "1500", "product_name": "Techno", "quantity": "100"}
        self.product_not_found = {"product_name": "Revision", "category": "klb", "quantity": 100, "price": 1500}
        self.product_err_data = {"product_name": "Revision English", "category": "Good book", "quantity": 100,
                                 "price": "dkls"}
        self.add_sale = {"products": [{"product_name": "techno", "quantity": "10"}]}
        self.sale_excess_data = {"products": [{"product_name": "Techno", "quantity": "1000"}]}
        self.sale_err_data = {"products": [{"product_name": "Mathsets4", "quantity": "12"}]}


def teardown(self):
    drop_tables()
    self.sign_up_data = None
    self.login_data = None
    self.invalid_sign_up_data = None
    self.empty_login_data = None
    self.invalid_login_data = None
    self.result = None
    self.token = None
    self.headers = None
    self.category = None
    self.category_update = None
    self.add_product = None
    self.product_not_found = None
    self.product_err_data = None
