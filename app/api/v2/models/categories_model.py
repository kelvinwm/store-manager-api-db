import datetime

import psycopg2

from flask import make_response, jsonify, request
from flask_restful import reqparse
from app.api.v2.models.users_model import login_required
from app.api.v2.utils import Validate
from db_init import connection

now = datetime.datetime.now()


class Categories:
    """Categories functions"""

    def __init__(self):
        self.conn = connection()
        self.cur = self.conn.cursor()

    @login_required
    def get_all_categories(self, current_user, token):
        """Get all Categories"""
        categories = []
        try:
            self.cur.execute("SELECT id, category, date_created from categories")
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Nothing has been stored yet"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "Category": row[1],
                    "date": row[2]
                }
                categories.append(item)
            return make_response(jsonify({
                "All categories": categories
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))

    @login_required
    def add_category(self, current_user, token):
        """Create Category"""
        pars = reqparse.RequestParser()
        pars.add_argument("category", required=True, help="category key missing", location=['json'])
        data2 = pars.parse_args()
        validate = Validate(current_user['role'], "create a category")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        data = request.get_json()
        if not data or not data["category"]:
            return jsonify({"message": "Invalid entry"})
        try:
            insert_query = """INSERT INTO categories (category, date_created) VALUES (%s,%s)"""
            self.cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(data["category"].lower()))
            if self.cur.fetchone():
                return jsonify({"message": "category already exists"})
            self.cur.execute(insert_query, (data["category"].lower(), now))
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "category added successfully"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "message": "Error entering category"
            }))

    @login_required
    def update_category(self, category_id, current_user, token):
        """Modify category"""
        pars = reqparse.RequestParser()
        pars.add_argument("category", required=True, help="category key missing", location=['json'])
        data2 = pars.parse_args()
        validate = Validate(current_user['role'], "update category")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        data = request.get_json()
        if not data['category']:
            return jsonify({"Category": "Invalid entry"})
        try:
            query = "SELECT * FROM categories WHERE id ='{0}'".format(category_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Category not found"
                }), 200)
            sql = """ UPDATE categories SET category = %s WHERE id = %s"""
            self.cur.execute(sql, (data["category"].lower(), category_id))
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    @login_required
    def delete_category(self, category_id, current_user, token):
        """Delete category"""
        validate = Validate(current_user['role'], "delete category")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        try:
            self.cur.execute("SELECT * FROM categories WHERE id= '{0}'".format(category_id))
            if not self.cur.fetchone():
                return jsonify({"message": "Item does not exist"})
            query = "DELETE FROM categories WHERE id= '{0}'".format(category_id)
            self.cur.execute(query)
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "category deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "message": "Error deleting category"
            }))
