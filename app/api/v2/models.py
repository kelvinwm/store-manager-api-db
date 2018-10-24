import psycopg2
from flask import make_response, jsonify, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import jwt
import datetime
from db_init import connection

conn = connection()

app = Flask(__name__)
app.config["SECRET_KEY"] = "NOCSNDOCNnocnsodi"


# def login_required(func):
#     """Decode tokem"""
#
#     @functools.wraps(func)
#     def user_auth(*args, **kwargs):
#         token = None
#
#         if 'access-token' in request.headers:
#             token = request.headers['access-token']
#         if not token:
#             return "No token"
#         try:
#             data = jwt.decode(token, app.config["SECRET_KEY"])
#             current_user = data['username']
#         except:
#             return "Token is invalid"
#
#         return func(current_user, *args, **kwargs)
#
#     return user_auth


class Products:
    """Product functions"""

    # @login_required
    def get_all_products(current_user, self):
        products = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, product_name, description,  quantity, price, date_created from products")
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Nothing has been stored yet"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "product_name": row[1],
                    "description": row[2],
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
                "Message": error
            }))

    # @login_required
    def add_product(current_user, self, **args):
        if args["price"] < 0:
            # raise ValueError("price cannot be a negative number")
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if args["quantity"] < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        try:

            insert_query = """INSERT INTO products (product_name, description, quantity, price, date_created) VALUES (%s,%s,
            %s,%s,%s)"""
            cur = conn.cursor()
            cur.execute(insert_query, (args["product_name"], args["description"], args["quantity"], args["price"],
                                       "2013-05-05"))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product added successfully"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))

    # @login_required
    def get_one_product(current_user, self, product_id):
        products = []
        try:
            query = "SELECT * FROM products WHERE id =" + str(product_id)
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Item does not exist"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "product_name": row[1],
                    "description": row[2],
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
                "Message": error
            }))

    # @login_required
    def update_product(current_user, self, product_id, **kwargs):

        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
            }))
        try:
            sql = """ UPDATE products SET product_name = %s ,description=%s, quantity=%s, price=%s WHERE id = %s"""
            cur = conn.cursor()
            cur.execute(sql, (kwargs["product_name"], kwargs["description"], kwargs["quantity"],
                              kwargs["price"], product_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    # @login_required
    def delete_product(current_user, self, product_id):
        # if not current_user == "admin":
        #     return make_response(jsonify({
        #         "Message": "Permission denied"
        #     }))
        try:
            query = "DELETE FROM products WHERE id =" + str(product_id)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))


class Users:
    """Users class for registration and login"""
    def login(self):
        """A user can login and get a token"""
        data = request.get_json()
        if not data or not data["email"] or not data["password"]:
            return jsonify({"Message": "Please enter all credentials"})
        query = "SELECT * FROM users WHERE email=?"
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email= '{0}'".format(data["email"]))
        if cur.fetchone():
            cur.execute("SELECT password FROM users WHERE email= '{0}'".format(data["email"]))
            for row in cur.fetchall():
                if check_password_hash(row[0], data["password"]):
                    """generate token"""
                    cur.execute("SELECT role FROM users WHERE email= '{0}'".format(data["email"]))
                    for row in cur.fetchall():
                        token = jwt.encode({"username": row[0], 'exp': datetime.datetime.utcnow()
                                                                                + datetime.timedelta(minutes=60)},
                                           app.config["SECRET_KEY"])
                        return jsonify({"Token": token.decode('UTF-8')})
        return jsonify({"Message": "Invalid credentials"})

    # @login_required
    def add_user(current_user, self):
        """A user can signup"""
        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
            }))
        data = request.get_json()
        if not data["first_name"] or not data["password"] or not data["role"] or not data["last_name"] or not \
                data["email"]:
            return make_response(jsonify({"message": "Please enter all credentials"}))
        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")
        try:

            insert_query = """INSERT INTO users (first_name, last_name, email, role, password, date_created) VALUES
             (%s,%s, %s,%s,%s,%s)"""
            cur = conn.cursor()
            cur.execute(insert_query, (data["first_name"], data["last_name"], data["email"], data["role"], password,
                                       "2013-05-05"))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "User successfully registered"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Error": "Error registering"
            }))
