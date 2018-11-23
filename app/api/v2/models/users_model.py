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
app = Flask(__name__)
app.config["SECRET_KEY"] = "NOCSNDOCNnocnsodi"


def login_required(func):
    """Decode tokem"""

    @functools.wraps(func)
    def user_auth(*args):
        token = ""
        conn = connection()
        cur = conn.cursor()
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            cur.execute("SELECT * FROM blacklists WHERE token= '{0}'".format(token))
            if cur.fetchone():
                return jsonify({"message": "You are logged out, please login"})
        if token == "":
            return {"message": "Your time has expired, please login"}
        try:
            current_user = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return {"message": "Your time has expired, please login"}
        return func(*args, current_user, token)

    return user_auth


class Users:
    """Users class for registration and login"""

    def __init__(self):
        self.conn = connection()
        self.cur = self.conn.cursor()

    def login(self):
        """A user can login and get a token"""
        data = request.get_json()
        if not data or not data["email"] or not data["password"]:
            return jsonify({"message": "Please enter all credentials"})
        self.cur.execute("SELECT password FROM users WHERE email= '{0}'".format(data["email"]))
        for row in self.cur.fetchall():
            if check_password_hash(row[0], data["password"]):
                """generate token"""
                self.cur.execute("SELECT role FROM users WHERE email= '{0}'".format(data["email"]))
                for role in self.cur.fetchall():
                    new_token = jwt.encode({"role": role[0], "username": data["email"],
                                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=200)},
                                           app.config["SECRET_KEY"])
                    return jsonify({"Token": new_token.decode('UTF-8'), "role": role[0]})
        return jsonify({"message": "Invalid credentials"})

    @login_required
    def add_user(self, current_user, token):
        """A user can signup"""
        validate = Validate(current_user['role'], "sign up users")
        if validate.validate_user() != "true":
            return validate.validate_user()
        data = request.get_json()
        if not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$])', data["password"]):
            return jsonify({"message": "password should include a digit, Uppercase, lowercase and a special character"})
        if len(data["password"]) < 8:
            return jsonify({"message": "Password should be at least 8 characters"})
        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")
        try:
            self.cur.execute("SELECT * FROM users WHERE email= '{0}'".format(data["email"].lower()))
            if self.cur.fetchone():
                return jsonify({"message": "User already registered"})
            insert_query = """INSERT INTO users (first_name, last_name, email, role, password, date_created) VALUES
                         (%s,%s, %s,%s,%s,%s)"""
            self.cur.execute(insert_query,
                             (data["first_name"].lower(), data["last_name"].lower(), data["email"].lower(),
                              False, password, now))
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "User successfully registered"
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Error": "Error registering"
            }))

    def register_admin(self):
        """Signup Admin"""
        password = generate_password_hash('25s#sssA4', method="sha256")
        try:
            self.cur.execute("SELECT * FROM users WHERE email= '{0}'".format('peterkelvin@storemanager.com'))
            if self.cur.fetchone():
                pass
            insert_query = """INSERT INTO users (first_name, last_name, email, role, password, date_created) VALUES
                            (%s,%s, %s,%s,%s,%s)"""
            self.cur.execute(insert_query,
                             ('peter', 'kelvin', 'peterkelvin@storemanager.com', "true", password, now))
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            pass

    @login_required
    def log_out(self, current_user, token):
        """User logout"""
        try:
            insert_query = """INSERT INTO blacklists (token, date_created) VALUES (%s,%s)"""
            self.cur.execute(insert_query, (token, now))
            self.conn.commit()
            return make_response(jsonify({"message": "User logout successful"}), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": "Error blacklisting token"
            }))

    @login_required
    def get_all_users(self, current_user, token):
        """A user can get all users"""
        validate = Validate(current_user['role'], "view users")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        users = []
        try:
            self.cur.execute("SELECT id, first_name, last_name, email, role, date_created from users")
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Nothing has been stored yet"
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
                "message": error
            }))

    @login_required
    def get_one_user(self, user_id, current_user, token):
        """Get a single registered user by user_id"""
        global one_user
        users = []
        try:
            query = "SELECT * FROM users WHERE id ='{0}'".format(user_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "User does not exist"
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
                "message": error
            }))

    @login_required
    def update_user(self, user_id, current_user, token):
        """give admin right to a specific store attendant"""
        global email, first_name, last_name, user_role
        validate = Validate(current_user['role'], "update user data")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        data = request.get_json()
        try:
            query = "SELECT * FROM users WHERE id ='{0}'".format(user_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "User not found"
                }), 200)
            for row in rows:
                first_name = row[1]
                last_name = row[2]
                email = row[3]
                user_role = row[4]
            if "first_name" in data:
                if validate.validate_updates("first_name", data) != "done":
                    return validate.validate_updates("first_name", data)
                first_name = data["first_name"].lower()
            if "last_name" in data:
                if validate.validate_updates("last_name", data) != "done":
                    return validate.validate_updates("last_name", data)
                last_name = data["last_name"].lower()
            if "email" in data:
                if validate.validate_updates("email", data) != "done":
                    return validate.validate_updates("last_name", data)
                is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                    data["email"])
                if not is_valid:
                    return jsonify({"message": "Invalid email"})
                email = data["email"].lower()
            if "role" in data:
                user_role = data["role"].lower()
            if "" in data:
                return {"Alert": "Please enter key and value format data"}
            sql = """ UPDATE users SET first_name = %s ,last_name=%s, email=%s, role=%s WHERE id = %s"""
            self.cur.execute(sql, (first_name, last_name, email, user_role, user_id))
            self.conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return error


