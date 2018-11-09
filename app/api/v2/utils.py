import re

import psycopg2
from flask import abort, request, make_response, jsonify
from flask_restful import reqparse
from db_init import connection

conn = connection()
cur = conn.cursor()


class Validate:
    def validate_product(self, current_user, action):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", required=True, type=str, help={"message": "Invalid entry"},
                            location=['json'])
        parser.add_argument("price", required=True, type=int,
                            help="Invalid entry", location=['json'])
        parser.add_argument("category", required=True, help="Invalid entry", location=['json'])
        parser.add_argument("quantity", required=True, type=int,
                            help="Invalid entry", location=['json'])
        args = parser.parse_args()
        if current_user != "true":
            return make_response(jsonify({
                "Error": "You not allowed to " + action,
                "message": "Permission denied.Contact Admin"
            }))
        if not args['category']:
            return jsonify({"category": "Invalid entry"})
        if not args['product_name']:
            return jsonify({"product name": "Invalid entry"})
        if args["price"] < 0:
            return make_response(jsonify({
                "message": "price cannot be a negative number"
            }), 200)
        if args["quantity"] < 0:
            return make_response(jsonify({
                "message": "Quantity cannot be a negative number"
            }), 200)
        cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(args["category"].lower()))
        if not cur.fetchone():
            return jsonify({"message": "Invalid category"})
        return "true"

    def validate_user(self, current_user, action):
        if current_user != "true":
            return make_response(jsonify({
                "Alert": "You are not allowed to " + action,
                "message": "Permission denied.Contact Admin"
            }))
        data = request.get_json()
        if not data["first_name"] or not data["last_name"] or not data["email"]:
            return make_response(jsonify({"message": "Please enter all credentials"}))
        is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data["email"])
        if not is_valid:
            return jsonify({"message": "Invalid email"})
        return "true"

    def admin_checker(self, current_user, action):
        if current_user != "true":
            return make_response(jsonify({
                "Denied": "You are not allowed to " + action,
                "message": "Permission denied.Contact Admin"
            }))
        return "true"

    def find_product(self, product_id):
        data = request.get_json()
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Item does not exist"
                }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "message": "error finding item"
            }))

        return "true"

    def validate_sale(self, products):

        global quantity, product_name
        for product in products:
            if not product["quantity"] or not product["product_name"]:
                return {"Error": "Empty entry"}
            if int(product["quantity"]) < 0:
                return {"Error": "Quantity cannot be a negative number"}
            query = "SELECT * FROM products WHERE product_name ='{0}'".format(product["product_name"].lower())
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return {"Error": "Product " + product["product_name"] + " does not exist",
                        "message": "Add this product"}
            for row in rows:
                product_name = row[1]
                quantity = int(row[3])
            if int(product["quantity"]) > quantity:
                return {"message": product["product_name"] + " out of stock",
                        "Remaining " + product_name: quantity, "Hint": "restock"}
        return "ok"
