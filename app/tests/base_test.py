import json
import unittest

from app import create_app


class BaseTest(unittest.TestCase):
    """TEST CLASS FOR AUTHENTICATION API ENDPOINTS"""

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.sign_up_data = {"first_name": "BEN10", "last_name": "THE4TH", "email": "ben100@storemanager.com",
                             "password": "25s#sssA4"}
        self.login_data = {"email": "peterkelvin@storemanager.com", "password": "25s#sssA4"}
        self.invalid_sign_up_data = {"first_name": "BEN10", "last_name": "THE4TH", "email": "ben10storemanager.com",
                                     "password": "25s#sssA4"}
        self.empty_login_data = {"email": "", "password": ""}
        self.invalid_login_data = {"username": "kevo", "email": "prince@gmail.com", "password": "12ds9vs33"}
        self.result = self.app.post('/api/v2/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.token = json.loads(self.result.data.decode('utf-8'))["Token"]
        self.headers = {'content-type': 'application/json', 'access-token': self.token}
        self.category = {"category": "KLB"}
        self.category_update = {"category": "CHEM"}
        self.add_product = {"product_name": "Jesma2", "category": "Longhorn", "quantity": 100, "price": 1500}
        self.product_not_found = {"product_name": "Revision", "category": "Longhorn", "quantity": 100, "price": 1500}
        self.product_err_data = {"product_name": "Revision English", "category": "Good book", "quantity": 100,
                                 "price": "dkls"}
