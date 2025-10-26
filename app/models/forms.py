from flask_wtf import FlaskForm
from flask_login import login_user
from wtforms import StringField, PasswordField, SubmitField, Field
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from ..models.model import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login In')
    
    def validate_email(self, field:Field):
        email = field.data
        user_email:User = User.query.filter_by(email=email).first()
        if not user_email:
            raise ValidationError("Email does not exist")
        self.user = user_email
        
    def validate_password(self, field:Field):
        paswrd = field.data
        if hasattr(self, "user"):
            if not self.user.check_password(paswrd):
                raise ValidationError("Wrong password")
        if hasattr(self, "user"):
            login_user(self.user)
            
        

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10, message="Username too short or long (3 to 10 characters needed)")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="The password is too short")])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo("password", "Password does not match")])
    submit = SubmitField('Register')
    
    def validate_username(self, field:Field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError("username already exist Log In")
     
    def validate_email(self, field:Field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError("Email already exist Log In")
     
    

            
    

