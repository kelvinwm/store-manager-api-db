import json
from app.tests.test import BaseTest
from db_init import drop_tables, create_tables


class TestSales(BaseTest):

    def test_get_all_sales(self):
        """TEST API can return all sales in the list"""
        response = self.app.get('/api/v2/sales', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_sale(self):
        """TEST API can add sale to list properly"""
        response = self.app.post('/api/v2/sales', data=json.dumps(self.add_sale), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Sales created successfully')
        self.assertEqual(response.status_code, 201)

    def test_invalid_add_sale(self):
        """TEST API can add sale to list properly"""
        response = self.app.post('/api/v2/sales', data=json.dumps(self.sale_err_data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Add this product')

    def test_excess_quantity_sale(self):
        """TEST API can add sale to list properly"""
        response = self.app.post('/api/v2/sales', data=json.dumps(self.sale_excess_data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Hint"], 'restock')

    def test_get_one_sale(self):
        """TEST API can get a single sale"""
        result = self.app.get('/api/v2/sales/1', headers=self.headers)
        self.assertEqual(result.status_code, 200)
        response = self.app.get('/api/v2/sales/1111', headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Item does not exist")

    def test_sale_list_can_be_edited(self):
        """TEST API can edit existing sale list"""
        result = self.app.put('/api/v2/sales/2', data=json.dumps(self.add_sale), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        res = self.app.put('/api/v2/sales/281', data=json.dumps(self.add_sale), headers=self.headers)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Product not found')

    def test_sale_list_deletion(self):
        """TEST API can delete existing sale list item"""
        result = self.app.delete('/api/v2/sales/2', data=json.dumps(self.add_sale), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        res = self.app.get('/api/v2/sales/2', data=json.dumps(self.add_sale), headers=self.headers)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Item does not exist')
