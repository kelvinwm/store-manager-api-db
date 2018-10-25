import re

import psycopg2
from flask import make_response, jsonify, request, Flask
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import jwt
import datetime
from db_init import connection

now = datetime.datetime.now()
conn = connection()

app = Flask(__name__)
app.config["SECRET_KEY"] = "NOCSNDOCNnocnsodi"


def login_required(func):
    """Decode tokem"""
    @functools.wraps(func)
    def user_auth(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']
            cur = conn.cursor()
            cur.execute("SELECT * FROM blacklists WHERE token= '{0}'".format(token))
            if cur.fetchone():
                return jsonify({"Message": "Token blacklisted, please login"})
        if not token:
            return "No token"
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = data['username']
        except:
            return "Token is invalid"

        return func(current_user, token, *args, **kwargs)

    return user_auth


class Products:
    """Product functions"""
    @login_required
    def get_all_products(current_user, token, self):
        """get all products"""
        products = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, product_name, category,  quantity, price, date_created from products")
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Nothing has been stored yet"
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
                "Message": error
            }))

    @login_required
    def add_product(current_user, token, self, **args):
        """add a product"""
        if not args['category'] or not args['product_name'] or args['quantity'] < 1 or args['price'] < 1:
            return jsonify({"Message": "Invalid entry"})
        if args["price"] < 0:
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if args["quantity"] < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        try:
            insert_query = """INSERT INTO products (product_name, category, quantity, price, date_created) VALUES (%s,%s,
            %s,%s,%s)"""
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE product_name= '{0}'".format(args["product_name"]))
            if cur.fetchone():
                return jsonify({"Message": "Product already exists"})
            cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(args["category"]))
            if not cur.fetchone():
                return jsonify({"Message": "Invalid category"})
            cur.execute(insert_query, (args["product_name"], args["category"], args["quantity"], args["price"], now))
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

    @login_required
    def get_one_product(current_user, token, self, product_id):
        """get one product"""
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
                "Message": error
            }))

    @login_required
    def update_product(current_user, token, self, product_id, **kwargs):
        """modify products"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        if not kwargs['category'] or not kwargs['product_name'] or kwargs['quantity'] < 1 or kwargs['price'] < 1:
            return jsonify({"Message": "Invalid entry"})
        if kwargs["price"] < 0:
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if kwargs["quantity"] < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        try:
            sql = """ UPDATE products SET product_name = %s ,category=%s, quantity=%s, price=%s WHERE id = %s"""
            cur = conn.cursor()
            query = "SELECT * FROM products WHERE id =" + str(product_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Product not found"
                }), 200)

            cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(kwargs["category"]))
            if not cur.fetchone():
                return jsonify({"Message": "Invalid category"})
            cur.execute(sql, (kwargs["product_name"], kwargs["category"], kwargs["quantity"],
                              kwargs["price"], product_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    @login_required
    def delete_product(current_user, token, self, product_id):
        """delete a product"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id= '{0}'".format(product_id))
            if not cur.fetchone():
                return jsonify({"Message": "Item does not exist"})
            query = "DELETE FROM products WHERE id= '{0}'".format(product_id)
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

    @login_required
    def add_user(current_user, token, self):
        """A user can signup"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        data = request.get_json()
        if not data["first_name"] or not data["password"] or not data["last_name"] or not data["email"]:
            return make_response(jsonify({"message": "Please enter all credentials"}))

        is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data["email"])
        if not is_valid or not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$])', data["password"]) \
                or len(data["password"]) > 12:
            return jsonify({"Message": "Invalid email or password"})

        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email= '{0}'".format(data["email"]))
            if cur.fetchone():
                return jsonify({"Message": "User already registered"})

            insert_query = """INSERT INTO users (first_name, last_name, email, role, password, date_created) VALUES
                         (%s,%s, %s,%s,%s,%s)"""
            cur.execute(insert_query, (data["first_name"], data["last_name"], data["email"], False, password, now))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "User successfully registered"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Error": "Error registering"
            }))

    @login_required
    def log_out(curreent_user, token, self):
        """User logout"""
        try:
            insert_query = """INSERT INTO blacklists (token, date_created) VALUES (%s,%s)"""
            cur = conn.cursor()
            cur.execute(insert_query, (token, now))
            conn.commit()
            conn.close()
            return make_response(jsonify({"Message": "User logout successful"}), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Error blacklisting token"
            }))

    @login_required
    def get_all_users(current_user, token, self):
        """A user can get all users"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        users = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, first_name, last_name, email, role, date_created from users")
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Nothing has been stored yet"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "role": row[4],
                    "date_created": row[5]
                }
                users.append(item)
            return make_response(jsonify({
                "All products": users
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))

    @login_required
    def get_one_user(current_user, token, self, user_id):
        """Get a single registered user by user_id"""
        users = []
        try:
            query = "SELECT * FROM users WHERE id =" + str(user_id)
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "User does not exist"
                }), 200)
            for row in rows:
                user = {
                    "Id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "role": row[4]
                }
                users.append(user)
            return make_response(jsonify({
                "status": "OK",
                "product": user
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))

    @login_required
    def update_user(current_user, token, self, user_id):
        """give admin right to a specific store attendant"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        data = request.get_json()
        if not data["first_name"] or not data["last_name"] or not data["email"] or not data["role"]:
            return make_response(jsonify({"message": "Please enter all credentials"}))

        is_valid = validate_email(data["email"])
        if not is_valid:
            return jsonify({"Message": "Invalid email or password"})
        try:
            sql = """ UPDATE users SET first_name = %s ,last_name=%s, email=%s, role=%s WHERE id = %s"""
            cur = conn.cursor()
            cur.execute(sql, (data["first_name"], data["last_name"], data["email"], data["role"], user_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error


class Categories:
    """Categories functions"""

    @login_required
    def get_all_categories(current_user, token, self):
        """Get all Categories"""
        categories = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, category, date_created from categories")
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Nothing has been stored yet"
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
                "Message": error
            }))

    @login_required
    def add_category(current_user, token, self):
        """Create Category"""
        data = request.get_json()
        if not data or not data["category"]:
            return jsonify({"Message": "Invalid entry"})
        try:
            insert_query = """INSERT INTO categories (category, date_created) VALUES (%s,%s)"""
            cur = conn.cursor()
            cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(data["category"]))
            if cur.fetchone():
                return jsonify({"Message": "category already exists"})
            cur.execute(insert_query, (data["category"], now))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "category added successfully"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Message": "Error entering category"
            }))

    @login_required
    def update_category(current_user, token, self, category_id):
        """Modify category"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        data = request.get_json()
        if not data['category']:
            return jsonify({"Message": "Invalid entry"})
        try:
            sql = """ UPDATE categories SET category = %s WHERE id = %s"""
            cur = conn.cursor()
            cur.execute(sql, (data["category"], category_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    @login_required
    def delete_category(current_user, token, self, category_id):
        """Delete category"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact Admin"
            }))
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM categories WHERE id= '{0}'".format(category_id))
            if not cur.fetchone():
                return jsonify({"Message": "Item does not exist"})
            query = "DELETE FROM categories WHERE id= '{0}'".format(category_id)
            cur.execute(query)
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "category deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Message": "Error deleting category"
            }))
