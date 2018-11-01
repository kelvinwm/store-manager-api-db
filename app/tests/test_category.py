import json

from app import create_app
from app.tests.base_test import BaseTest
from db_init import delete_category, create_tables


class TestCategories(BaseTest):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.resul = self.app.post('/api/v2/auth/login',
                                    data=json.dumps({"email": "peterkelvin@storemanager.com", "password": "25s#sssA4"}),
                                    content_type='application/json')
        self.toke = json.loads(self.resul.data.decode('utf-8'))["Token"]
        self.header = {'content-type': 'application/json', 'access-token': self.toke}
    def test_get_all_categories(self):
        """TEST API can return all categories in the database"""
        response = self.app.get('/api/v2/category', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_add_category(self):
        """TEST API can add category to database properly"""
        delete_category()
        create_tables()
        response = self.app.post('/api/v2/category', data=json.dumps(self.category), headers=self.header)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "category added successfully")
        self.assertEqual(response.status_code, 201)

    def test_category_list_can_be_edited(self):
        """TEST API can edit existing category list"""
        response = self.app.put('/api/v2/category/1', data=json.dumps({"category": "klb"}), headers=self.header)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Updated successfully')
        self.assertEqual(response.status_code, 200)

    def test_delete_category(self):
        """TEST API can delete existing category list item"""
        result = self.app.delete('/api/v2/category/50', headers=self.header)
        self.assertEqual(result.status_code, 200)
