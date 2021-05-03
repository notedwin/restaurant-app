from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from wtforms import validators
from app.model import User

class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
  first_name = StringField('First Name', 
                 [validators.DataRequired()])
  last_name = StringField('Last Name', 
                 [validators.DataRequired()])
  email = StringField('Email Address', [validators.DataRequired(), 
             validators.Email(), validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', 
                           message='Passwords must match')
        ])
  confirm_password = PasswordField('Repeat Password')
  submit = SubmitField('Sign Up')

  def validate_email(self,email):
    email = User.query.filter_by(email=email.data).first()
    if email:
      raise ValidationError('Email already in Use.')

class CheckoutForm(FlaskForm):
  full_name = StringField('Full', 
                 [validators.DataRequired()])
  email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Length(min=6, max=35)])
  address = StringField('Address', [validators.DataRequired()])
  country = StringField('Country', [validators.DataRequired()])
  state = StringField('State', [validators.DataRequired()])
  zip_code = StringField('Zip', [validators.DataRequired(), validators.Length(min=4,max=6)])
  # could populate from ENUM
  orderType = SelectField('How do you want your food?', choices = [('dine','Dine-In'),('delivery','Delivery'),('pickup','Pick-up')])
  submit = SubmitField('Continue to Payment')