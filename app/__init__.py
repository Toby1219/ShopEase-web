from flask import Flask, jsonify, redirect, url_for
from .settings import BASE_PATH, jwt, db, login_manager
from .models.model import User
from datetime import datetime
app = Flask(__name__)

app.config.from_pyfile(f"{BASE_PATH}/settings.py")
app.config["JSON_SORT_KEYS"] = False

db.init_app(app)
jwt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "Authenticator:index"

def create_app():
    
    from .routes.api import ApiRoutes, ApiAuth, blacklist
    from .routes.views import Apiview, WebView
    from .routes.auth import Authenticator
    
    
    ApiRoutes.register(app)
    auth_api = ApiAuth.as_view("auth_api")
    app.add_url_rule("/api/auth", view_func=auth_api, methods=["GET", "POST", "PUT", "DELETE"])
    
    Apiview.register(app)
    WebView.register(app)
    Authenticator.register(app)

    with app.app_context():
        db.create_all()
 
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for("WebView:index"))
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

        
    # ==================================
    # JWT BLACKLIST AND ERROR HANDLERS
    # ==================================
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has been revoked"), 401


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has expired"), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(msg="Invalid token"), 422


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(msg="Missing Authorization Header"), 401


    # ==================================
    # JINJA COUSTOM FILTER
    # ==================================
    @app.template_filter('format_datetime')
    def format_datetime(value, format="%b %d, %Y %I:%M %p"):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        return value.strftime(format)
    
    @app.template_filter("shorten_text")
    def shorten_text(value:str):
        if isinstance(value, str):
            if len(value) >= 2:
                text = f"{" ".join(value.split()[:2])} ..."
        return text

    @app.template_filter("count_list")
    def count_list(value:list):
        if isinstance(value, list):
            value = len(value)
        return value
    return app

    