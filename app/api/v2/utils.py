import re
import psycopg2
from flask import make_response, jsonify
from flask_restful import reqparse
from db_init import connection




class Validate:
    def __init__(self, current_user, action):
        self.current_user = current_user
        self.action = action
        self.conn = connection()
        self.cur = self.conn.cursor()

    def validate_product(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", required=True, help="Invalid entry", location=['json'])
        parser.add_argument("price", required=True, type=int,
                            help="Invalid entry", location=['json'])
        parser.add_argument("category", required=True, help="Invalid entry", location=['json'])
        parser.add_argument("quantity", required=True, type=int,
                            help="Invalid entry", location=['json'])
        args = parser.parse_args()
        if self.current_user != "true":
            return make_response(jsonify({
                "Error": "You not allowed to " + self.action,
                "Message": "Permission denied.Contact Admin"
            }))
        if not args['category']:
            return jsonify({"category": "Invalid entry"})
        if not args['product_name']:
            return jsonify({"product name": "Invalid entry"})
        if args["price"] < 0:
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if args["quantity"] < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        self.cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(args["category"].lower()))
        if not self.cur.fetchone():
            return jsonify({"Message": "Invalid category"})
        return "true"

    def validate_user(self):
        if self.current_user != "true":
            return make_response(jsonify({
                "Alert": "You are not allowed to " + self.action,
                "Message": "Permission denied.Contact Admin"
            }))
        parser = reqparse.RequestParser()
        parser.add_argument("first_name", required=True, help="first name empty", location=['json'])
        parser.add_argument("last_name", required=True, help="last name empty", location=['json'])
        parser.add_argument("email", required=True, help="empty email", location=['json'])
        parser.add_argument("password", required=True, help="empty password", location=['json'])
        data = parser.parse_args()
        if not data["first_name"] or not data["last_name"]:
            return {"Error": "First name or last name fields empty"}
        if not data["email"]:
            return make_response(jsonify({"message": "Please enter email"}))
        is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data["email"])
        if not is_valid:
            return jsonify({"Message": "Invalid email"})
        return "true"

    def admin_checker(self):
        if self.current_user != "true":
            return make_response(jsonify({
                "Denied": "You are not allowed to " + self.action,
                "Message": "Permission denied.Contact Admin"
            }))
        return "true"

    def find_product(self, product_id):
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Item does not exist"
                }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Message": "error finding item"
            }))

        return "true"

    def validate_sale(self, products):
        global quantity, product_name
        for product in products:
            if "quantity" not in product or "product_name" not in product:
                return {"Alert": "Quantity or product_name key missing"}
            if not product["quantity"] or not product["product_name"]:
                return {"Error": "quantity or product name cannot be empty"}
            if int(product["quantity"]) < 0:
                return {"Error": "Quantity cannot be a negative number"}
            query = "SELECT * FROM products WHERE product_name ='{0}'".format(product["product_name"].lower())
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return {"Error": "Product " + product["product_name"] + " does not exist",
                        "Message": "Add this product"}
            for row in rows:
                product_name = row[1]
                quantity = int(row[3])
            if int(product["quantity"]) > quantity:
                return {"Message": product["product_name"] + " out of stock",
                        "Remaining " + product_name: quantity, "Hint": "restock"}
        return "ok"

    def validate_updates(self, key_value, data):
        if not data[key_value]:
            return {"Alert": "please enter " + key_value}
        if key_value == "quantity" or key_value == "price":
            if int(data[key_value]) < 0:
                return key_value + " cannot be a negative value"
        return "done"

    def validate_get_sales(self, current_user):
        if current_user["role"] == "true":
            self.cur.execute("SELECT id, username, product_id, quantity, price, date_created from sales")
            rows = self.cur.fetchall()
            return rows
        else:
            query = "SELECT * FROM sales WHERE username ='{0}'".format(current_user["username"])
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
