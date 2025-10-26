from pathlib import Path
from decouple import config
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager
from flask_jwt_extended import JWTManager

BASE_PATH = Path(__file__).resolve().parent


db  = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()


# Secret key for securely signing the session cookie and other secrets
SECRET_KEY = config("SECRETE_KEY")  # Should be a long, random string

# Database connection URL
SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")  # Example: "sqlite:///site.db" or a PostgreSQL URL

# Enables or disables SQLAlchemy's event system (track modifications)
SQLALCHEMY_TRACK_MODIFICATION = config("SQLALCHEMY_TRACK_MODIFICATION")  # Should typically be "False"

# Secret key for JWT authentication
JWT_SECRET_KEY = config("JWT_SECRETE_KEY")  # Should be a long, random string for signing JWT tokens

# Enables or disables JWT token blacklisting
JWT_BLACKLIST_ENABLED = config("JWT_BLACKLIST_ENABLED")  # Should be "True" or "False"

# Determines which types of tokens (access, refresh) to check against the blacklist
JWT_BLACKLIST_TOKEN_CHECKS = config("JWT_BLACKLIST_TOKEN_CHECKS")  # Example: "access, refresh"

# Expiration time for access tokens
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=float(config("JWT_ACCESS_TOKEN_EXPIRES")))

# Expiration time for refresh tokens
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=float(config("JWT_REFRESH_TOKEN_EXPIRES")))
# Adjust as needed for security and usability

# Domain URL for the application
DOMAIN_URL = "http://127.0.0.1:5000"  # Update this if deploying to a live server

REMEMBER_COOKIE_DURATION = timedelta(days=int(config("REMEMBER_COOKIE_DURATION")))

PER_PAGE:int = 3
