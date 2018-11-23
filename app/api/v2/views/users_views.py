from flask import jsonify, make_response, Blueprint
from flask_restful import Resource, Api
from app.api.v2.models.users_model import Users


class UserLogin(Resource):
    """A user can Login"""

    def __init__(self):
        self.users = Users()

    def post(self):
        return self.users.login()


class UserSignup(Resource):
    """Register a user"""

    def __init__(self):
        self.users = Users()

    def post(self):
        return self.users.add_user()


class UserLogout(Resource):
    """Log out a user"""

    def __init__(self):
        self.users = Users()

    def get(self):
        return self.users.log_out()


class Home(Resource):
    """Home page"""

    def __init__(self):
        pass

    def get(self):
        return make_response(jsonify({"Message": " Welcome to store manager api"}), 200)


class AllUserInformation(Resource):
    """Get registered users"""

    def __init__(self):
        self.users = Users()

    def get(self):
        return self.users.get_all_users()


class SingleUserInformation(Resource):
    """Get and modify user"""

    def __init__(self):
        self.users = Users()

    def get(self, user_id):
        return self.users.get_one_user(user_id)

    def put(self, user_id):
        return self.users.update_user(user_id)


landing_page = Blueprint("landing_page", __name__)
api = Api(landing_page)
api.add_resource(Home, '/', endpoint="landing page")
