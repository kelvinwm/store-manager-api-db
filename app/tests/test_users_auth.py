import unittest
import json

from app.tests.base_test import BaseTest
from db_init import delete_record


class TestUsersAuth(BaseTest):
    """TEST CLASS FOR AUTHENTICATION API ENDPOINTS"""

    def test_valid_signup(self):
        """TEST API can sign up users correctly"""
        delete_record(self.sign_up_data["email"])
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(self.sign_up_data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "User successfully registered")

    def test_valid_login(self):
        """TEST API can sign up users correctly"""
        self.result = self.app.post('/api/v2/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.assertEqual(self.result.status_code, 200)

    def test_invalid_signup(self):
        """TEST invalid email"""
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(self.invalid_sign_up_data),
                                 headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Invalid email")

    def test_empty_credentials_login(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v2/auth/login', data=json.dumps(self.empty_login_data),
                                 content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Please enter all credentials")

    def test_invalid_login(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v2/auth/login', data=json.dumps(self.invalid_login_data),
                                 content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Invalid credentials")
