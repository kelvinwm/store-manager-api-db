import unittest
import json

from app import create_app
from db_init import drop


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        drop()
        self.data = {"product_name": "Jesma",
                     "category": "Longhorn",
                     "quantity": 100,
                     "price": 1500
                     }
        self.data_not_found = {"product_name": "Revision",
                               "category": "Longhornn",
                               "quantity": 100,
                               "price": 1500
                               }
        self.err_data = {"product_name": "Revision English",
                         "category": "Good book",
                         "quantity": 100,
                         "price": "dkls"
                         }
        self.login_data = {
            "email": "storeowner@storemanager.com",
            "password": "233#SFdsm@"
        }
        self.result = self.app.post('/api/v2/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.token = json.loads(self.result.data.decode('utf-8'))["Token"]
        self.headers = {'content-type': 'application/json', 'access-token': self.token}

    def test_get_all_items(self):
        """TEST API can return all products in the list"""
        response = self.app.get('/api/v2/products', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        """TEST API can add product to list properly"""
        response = self.app.post('/api/v2/products', data=json.dumps(self.data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Product added successfully")
        self.assertEqual(response.status_code, 201)

    def test_invalid_add_product(self):
        """TEST API can add product to list properly"""
        response = self.app.post('/api/v2/products', data=json.dumps(self.err_data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'message': {'price': 'Invalid entry'}})

    def test_get_one_product(self):
        """TEST API can get a single product"""
        result = self.app.get('/api/v2/products/1', headers=self.headers)
        self.assertEqual(result.status_code, 200)
        response = self.app.get('/api/v2/products/11', headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Item does not exist")

    # def test_product_list_can_be_edited(self):
    #     """TEST API can edit existing product list"""
    #     result = self.app.put('/api/v2/products/2', data=json.dumps(self.data), headers=self.headers)
    #     self.assertEqual(result.status_code, 200)
    #     res = self.app.put('/api/v2/products/21', data=json.dumps(self.data_not_found), headers=self.headers)
    #     result = json.loads(res.data.decode('utf-8'))
    #     self.assertEqual(result["Message"], 'Product not found')

    #
    def test_product_list_deletion(self):
        """TEST API can delete existing product list item"""
        result = self.app.delete('/api/v2/products/2', data=json.dumps(self.data), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        # res = self.app.get('/api/v2/products/2', data=json.dumps(self.data), headers=self.headers)
        # result = json.loads(res.data.decode('utf-8'))
        # self.assertEqual(result, {'Product': 'Product not found', 'status': 'OK'})