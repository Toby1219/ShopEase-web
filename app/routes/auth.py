from flask_classful import FlaskView, route
from flask_login import logout_user
from flask import render_template, redirect, url_for, session
from ..models.forms import LoginForm, RegisterForm
from ..models.model import User

class Authenticator(FlaskView):
    route_base = "/auth/"
    
    def __init__(self):
        super().__init__()
        self.context = {}
    
    def index(self):
        form_login = LoginForm()
        form_reg = RegisterForm()
        tab = session.get("tab", "login")
        return render_template("auth/auth.html", form_login=form_login, form_reg=form_reg, context=self.context, tab=tab)

    @route("/log-in", methods=["GET", "POST"])
    def user_login_in(self):
        form_login = LoginForm()
        if form_login.validate_on_submit():
            return redirect(url_for("WebView:index"))
        
        self.context["email_error"] = form_login.email.errors
        self.context["pwrd_error"] = form_login.password.errors
        session["tab"] = "login"
        return self.index()
        
    @route("/register", methods=["GET", "POST"])
    def user_register(self):
        form_reg = RegisterForm()
        username = form_reg.data.get("username")
        email = form_reg.data.get("email")
        password = form_reg.data.get("password")
        # confirm_password = form_reg.data.get("confirm_password")
        if form_reg.validate_on_submit():
            user = User(username=username, email=email, pwrd_text=password)
            user.set_password(password)
            user.create_user()
            return redirect(url_for("Apiview:home"))
        
        self.context["username_error"] = form_reg.username.errors
        self.context["email_error"] = form_reg.email.errors
        self.context["password_error"] = form_reg.password.errors
        self.context["confirm_password_error"] = form_reg.confirm_password.errors 
        session["tab"] = "register"
        return self.index() 
    
    
    @route("/logout")
    def user_logout(self):
        logout_user()
        return redirect(url_for("Authenticator:index"))

        
        
        
        

