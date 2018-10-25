from flask import Flask, make_response, jsonify
from db_init import create_tables


def create_app():
    app = Flask(__name__)
    create_tables()
    from app.api.v2 import version_2 as v2
    from app.api.v2.views import landing_page
    app.register_blueprint(v2, url_prefix="/api/v2")
    app.register_blueprint(landing_page)

    @app.errorhandler(404)
    def not_found(e):
        # defining function
        return make_response(jsonify({
            "Message": "Route not found. Please check on the route"
        }), 200)

    @app.errorhandler(500)
    def internal_error(error):
        return make_response(jsonify({
            "Message": "Internal server"
        }), 200)

    return app
