import datetime
import psycopg2
from flask import jsonify, make_response, request
from app.api.v2.models.users_model import login_required
from app.api.v2.utils import Validate
from db_init import connection

now = datetime.datetime.now()


class ProductsModel:
    """Product functions"""

    def __init__(self):
        self.conn = connection()
        self.cur = self.conn.cursor()

    @login_required
    def get_all_products(self, current_user, token):
        """get all products"""
        products = []
        try:
            self.cur.execute("SELECT id, product_name, category,  quantity, price, date_created from products")
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Nothing has been stored yet"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "quantity": int(row[3]),
                    "price": int(row[4]),
                    "date": row[5]
                }
                products.append(item)
            return make_response(jsonify({
                "All products": products
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))

    @login_required
    def add_product(self, current_user, token):
        """add a product"""
        data = request.get_json()
        validate = Validate(current_user['role'], "Add product")
        if validate.validate_product() != "true":
            return validate.validate_product()

        try:
            insert_query = """INSERT INTO products (product_name, category, quantity, price, date_created) VALUES (%s,
            %s,%s,%s,%s)"""
            self.cur.execute("SELECT * FROM products WHERE product_name= '{0}'".format(data["product_name"].lower()))
            if self.cur.fetchone():
                return jsonify({"message": "Product already exists"})
            self.cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(data["category"].lower()))
            if not self.cur.fetchone():
                return jsonify({"message": "Invalid category"})
            self.cur.execute(insert_query, (data["product_name"].lower(), data["category"].lower(),
                                            data["quantity"].lower(), data["price"].lower(), now))
            self.conn.commit()
            return make_response(jsonify({
                "product": data,
                "message": "Product added successfully"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))

    @login_required
    def get_one_product(self, product_id, current_user, token):
        """get one product"""
        products = []
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Item does not exist"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "quantity": int(row[3]),
                    "price": int(row[4]),
                    "date": row[5]
                }
                products.append(item)
            return make_response(jsonify({
                "status": "OK",
                "product": products
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))

    @login_required
    def update_product(self, product_id, current_user, token):
        """modify products"""
        global price, category, quantity
        validate = Validate(current_user['role'], "Update product")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        data = request.get_json()
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Product not found"
                }), 200)
            for row in rows:
                category = row[2]
                quantity = int(row[3])
                price = int(row[4])
            if "product_name" in data:
                if validate.validate_updates("product_name", data) != "done":
                    return validate.validate_updates("product_name", data)
                return {"Error": "You cannot update product name"}
            if "category" in data:
                if validate.validate_updates("category", data) != "done":
                    return validate.validate_updates("category", data)
                category = data["category"].lower()
            if "quantity" in data:
                if validate.validate_updates("quantity", data) != "done":
                    return validate.validate_updates("quantity", data)
                quantity = data["quantity"]
            if "price" in data:
                if validate.validate_updates("price", data) != "done":
                    return validate.validate_updates("price", data)
                price = data["price"]
            if "" in data:
                return {"Alert": "Please enter key and value format data"}
            sql = """ UPDATE products SET category=%s, quantity=%s, price=%s WHERE id = %s"""
            if validate.find_product(product_id) != "true":
                return validate.find_product(product_id)
            self.cur.execute(sql, (category, quantity, price, product_id))
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return {"Error": "Unable to update product try again!"}

    @login_required
    def delete_product(self, product_id, current_user, token):
        """delete a product"""
        validate = Validate(current_user['role'], "delete product")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        try:
            if validate.find_product(product_id) != "true":
                return validate.find_product(product_id)
            query = "DELETE FROM products WHERE id= '{0}'".format(product_id)
            self.cur.execute(query)
            self.conn.commit()
            return make_response(jsonify({
                "message": "Product deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))
