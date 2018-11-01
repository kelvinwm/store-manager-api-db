import re
import psycopg2
from flask import make_response, jsonify, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import jwt
import datetime

from app.api.v2.utils import Validate
from db_init import connection

now = datetime.datetime.now()
conn = connection()
Token = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "NOCSNDOCNnocnsodi"
cur = conn.cursor()


def login_required(func):
    """Decode tokem"""

    @functools.wraps(func)
    def user_auth(*args):
        global token
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            cur.execute("SELECT * FROM blacklists WHERE token= '{0}'".format(token))
            if cur.fetchone():
                return jsonify({"Message": "You are logged out, please login"})
        if not token:
            return "No token"
        try:
            current_user = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return {"Message": "Your time has expired, please login"}
        return func(*args, current_user, token)

    return user_auth


class Products:
    """Product functions"""

    @login_required
    def get_all_products(self, current_user, token):
        """get all products"""
        products = []
        try:
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
    def add_product(self, current_user, token):
        """add a product"""
        if Validate().validate_product(current_user['role'], "Add product") != "true":
            return Validate().validate_product(current_user['role'], "Add product")
        data = request.get_json()
        try:
            insert_query = """INSERT INTO products (product_name, category, quantity, price, date_created) VALUES (%s,
            %s,%s,%s,%s)"""
            cur.execute("SELECT * FROM products WHERE product_name= '{0}'".format(data["product_name"].lower()))
            if cur.fetchone():
                return jsonify({"Message": "Product already exists"})
            cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(data["category"].lower()))
            if not cur.fetchone():
                return jsonify({"Message": "Invalid category"})
            cur.execute(insert_query, (data["product_name"].lower(), data["category"].lower(), data["quantity"].lower(),
                                       data["price"].lower(), now))
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
    def get_one_product(self, product_id, current_user, token):
        """get one product"""
        products = []
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
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
    def update_product(self, product_id, current_user, token):
        """modify products"""
        global price, category, quantity
        if Validate().admin_checker(current_user['role'], "Update product") != "true":
            return Validate().admin_checker(current_user['role'], "Update product")
        data = request.get_json()
        try:
            query = "SELECT * FROM products WHERE id ='{0}'".format(product_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Product not found"
                }), 200)
            for row in rows:
                category = row[2]
                quantity = int(row[3])
                price = int(row[4])
            if "product_name" in data:
                return {"Error": "You cannot update product name"}
            if "category" in data:
                category = data["category"].lower()
            if "quantity" in data:
                quantity = data["quantity"]
            if "price" in data:
                price = data["price"]
            sql = """ UPDATE products SET category=%s, quantity=%s, price=%s WHERE id = %s"""
            if Validate().find_product(product_id) != "true":
                return Validate().find_product(product_id)
            cur.execute(sql, (category, quantity, price, product_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return {"Error": "Unable to update product try again!"}

    @login_required
    def delete_product(self, product_id, current_user, token):
        """delete a product"""
        if Validate().admin_checker(current_user['role'], "delete product") != "true":
            return Validate().admin_checker(current_user['role'], "delete product")
        try:
            if Validate().find_product(product_id) != "true":
                return Validate().find_product(product_id)
            query = "DELETE FROM products WHERE id= '{0}'".format(product_id)
            cur.execute(query)
            conn.commit()
            return make_response(jsonify({
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
        cur.execute("SELECT password FROM users WHERE email= '{0}'".format(data["email"]))
        for row in cur.fetchall():
            if check_password_hash(row[0], data["password"]):
                """generate token"""
                cur.execute("SELECT role FROM users WHERE email= '{0}'".format(data["email"]))
                for role in cur.fetchall():
                    new_token = jwt.encode({"role": role[0], "username": data["email"],
                                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=7200)},
                                           "NOCSNDOCNnocnsodi")
                    return jsonify({"Token": new_token.decode('UTF-8')})
        return jsonify({"Message": "Invalid credentials"})

    @login_required
    def add_user(self, current_user, token):
        """A user can signup"""
        if Validate().validate_user(current_user['role'], "sign up users") != "true":
            return Validate().validate_user(current_user['role'], "sign up users")
        data = request.get_json()
        if not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$])', data["password"]):
            return jsonify({"Message": "password should include a digit, Uppercase, lowercase and a special character"})
        if len(data["password"]) < 8:
            return jsonify({"Message": "Password should be at least 8 characters"})
        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")
        try:
            cur.execute("SELECT * FROM users WHERE email= '{0}'".format(data["email"].lower()))
            if cur.fetchone():
                return jsonify({"Message": "User already registered"})
            insert_query = """INSERT INTO users (first_name, last_name, email, role, password, date_created) VALUES
                         (%s,%s, %s,%s,%s,%s)"""
            cur.execute(insert_query, (data["first_name"].lower(), data["last_name"].lower(), data["email"].lower(),
                                       False, password, now))
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
    def log_out(self, current_user, token):
        """User logout"""
        try:
            insert_query = """INSERT INTO blacklists (token, date_created) VALUES (%s,%s)"""
            cur.execute(insert_query, (token, now))
            conn.commit()
            return make_response(jsonify({"Message": "User logout successful"}), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Error blacklisting token"
            }))

    @login_required
    def get_all_users(self, current_user, token):
        """A user can get all users"""
        if Validate().admin_checker(current_user['role'], "view users") != "true":
            return Validate().admin_checker(current_user['role'], "view users")
        users = []
        try:
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
    def get_one_user(self, user_id, current_user, token):
        """Get a single registered user by user_id"""
        global one_user
        users = []
        try:
            query = "SELECT * FROM users WHERE id ='{0}'".format(user_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "User does not exist"
                }), 200)
            for row in rows:
                one_user = {
                    "Id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "role": row[4]
                }
                users.append(one_user)
            return make_response(jsonify({
                "User": one_user
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))

    @login_required
    def update_user(self, user_id, current_user, token):
        """give admin right to a specific store attendant"""
        global email, first_name, last_name, user_role
        if Validate().admin_checker(current_user['role'], "update user data") != "true":
            return Validate().admin_checker(current_user['role'], "update user data")
        data = request.get_json()
        try:
            query = "SELECT * FROM users WHERE id ='{0}'".format(user_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "User not found"
                }), 200)
            for row in rows:
                first_name = row[1]
                last_name = row[2]
                email = row[3]
                user_role = row[4]
            if "first_name" in data:
                first_name = data["first_name"].lower()

            if "last_name" in data:
                last_name = data["last_name"].lower()

            if "email" in data:
                is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                    data["email"])
                if not is_valid:
                    return jsonify({"Message": "Invalid email"})
                email = data["email"].lower()

            if "role" in data:
                user_role = data["role"].lower()

            sql = """ UPDATE users SET first_name = %s ,last_name=%s, email=%s, role=%s WHERE id = %s"""
            cur.execute(sql, (first_name, last_name, email, user_role, user_id))
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
    def get_all_categories(self, current_user, token):
        """Get all Categories"""
        categories = []
        try:
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
    def add_category(self, current_user, token):
        """Create Category"""
        if Validate().admin_checker(current_user['role'], "create a category") != "true":
            return Validate().admin_checker(current_user['role'], "create a category")
        data = request.get_json()
        if not data or not data["category"]:
            return jsonify({"Message": "Invalid entry"})
        try:
            insert_query = """INSERT INTO categories (category, date_created) VALUES (%s,%s)"""
            cur.execute("SELECT * FROM categories WHERE category= '{0}'".format(data["category"].lower()))
            if cur.fetchone():
                return jsonify({"Message": "category already exists"})
            cur.execute(insert_query, (data["category"].lower(), now))
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
    def update_category(self, category_id, current_user, token):
        """Modify category"""
        if Validate().admin_checker(current_user['role'], "update category") != "true":
            return Validate().admin_checker(current_user['role'], "update category")
        data = request.get_json()
        if not data['category']:
            return jsonify({"Category": "Invalid entry"})
        try:
            query = "SELECT * FROM categories WHERE id ='{0}'".format(category_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Category not found"
                }), 200)
            sql = """ UPDATE categories SET category = %s WHERE id = %s"""
            cur.execute(sql, (data["category"].lower(), category_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    @login_required
    def delete_category(self, category_id, current_user, token):
        """Delete category"""
        if Validate().admin_checker(current_user['role'], "delete category") != "true":
            return Validate().admin_checker(current_user['role'], "delete category")
        try:
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
