import re

from flask import abort, request, make_response, jsonify
from flask_restful import reqparse
from db_init import connection

conn = connection()


class Validate:
    def validate_product(self, current_user):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", required=True, help="Invalid entry", location=['json'])
        parser.add_argument("price", required=True, type=int,
                            help="Invalid entry", location=['json'])
        parser.add_argument("category", required=True, help="Invalid entry", location=['json'])
        parser.add_argument("quantity", required=True, type=int,
                            help="Invalid entry", location=['json'])
        args = parser.parse_args()
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        if not args['category'] or not args['product_name']:
            return jsonify({"Message": "Invalid entry"})
        if args["price"] < 0:
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if args["quantity"] < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(args["category"]))
        if not cur.fetchone():
            return jsonify({"Message": "Invalid category"})
        return "true"

    def validate_user(self, current_user):
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        data = request.get_json()
        if not data["first_name"] or not data["last_name"] or not data["email"]:
            return make_response(jsonify({"message": "Please enter all credentials"}))
        is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data["email"])
        if not is_valid:
            return jsonify({"Message": "Invalid email"})
        return "true"

    def admin_checker(self, current_user):
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        return "true"
