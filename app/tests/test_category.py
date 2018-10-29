import json
from app.tests.base_test import BaseTest
from db_init import delete_category


class TestCategories(BaseTest):

    def test_get_all_categories(self):
        """TEST API can return all categories in the database"""
        response = self.app.get('/api/v2/category', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_category(self):
        """TEST API can add category to database properly"""
        delete_category(self.category["category"])
        response = self.app.post('/api/v2/category', data=json.dumps(self.category), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "category added successfully")
        self.assertEqual(response.status_code, 201)

    def test_category_list_can_be_edited(self):
        """TEST API can edit existing category list"""
        response = self.app.put('/api/v2/category/21', data=json.dumps(self.category_update), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Updated successfully')
        self.assertEqual(response.status_code, 200)

    def test_delete_category(self):
        """TEST API can delete existing category list item"""
        result = self.app.delete('/api/v2/category/50', headers=self.headers)
        self.assertEqual(result.status_code, 200)
