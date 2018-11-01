# import json
# from app.tests.base_test import BaseTest
# from db_init import drop_tables, create_tables
#
#
# class TestProducts(BaseTest):
#
#     def test_get_all_items(self):
#         """TEST API can return all products in the list"""
#         response = self.app.get('/api/v2/products', headers=self.headers)
#         self.assertEqual(response.status_code, 200)
#
#     def test_add_product(self):
#         """TEST API can add product to list properly"""
#         drop_tables()
#         create_tables()
#         response = self.app.post('/api/v2/products', data=json.dumps(self.add_product), headers=self.headers)
#         result = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(result["Message"], "Product added successfully")
#         self.assertEqual(response.status_code, 201)
#
#     def test_invalid_add_product(self):
#         """TEST API can add product to list properly"""
#         response = self.app.post('/api/v2/products', data=json.dumps(self.product_err_data), headers=self.headers)
#         result = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(result, {'message': {'price': 'Invalid entry'}})
#
#     def test_get_one_product(self):
#         """TEST API can get a single product"""
#         result = self.app.get('/api/v2/products/1', headers=self.headers)
#         self.assertEqual(result.status_code, 200)
#         response = self.app.get('/api/v2/products/11', headers=self.headers)
#         result = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(result["Message"], "Item does not exist")
#
#     def test_product_list_can_be_edited(self):
#         """TEST API can edit existing product list"""
#         result = self.app.put('/api/v2/products/2', data=json.dumps(self.add_product), headers=self.headers)
#         self.assertEqual(result.status_code, 200)
#         res = self.app.put('/api/v2/products/21', data=json.dumps(self.product_not_found), headers=self.headers)
#         result = json.loads(res.data.decode('utf-8'))
#         self.assertEqual(result["Message"], 'Item does not exist')
#
#     def test_product_list_deletion(self):
#         """TEST API can delete existing product list item"""
#         result = self.app.delete('/api/v2/products/2', data=json.dumps(self.add_product), headers=self.headers)
#         self.assertEqual(result.status_code, 200)
#         res = self.app.get('/api/v2/products/2', data=json.dumps(self.add_product), headers=self.headers)
#         result = json.loads(res.data.decode('utf-8'))
#         self.assertEqual(result["Message"], 'Item does not exist')
