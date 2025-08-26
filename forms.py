from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[Length(max=15)])
    role = SelectField('Role', choices=[
        ('restaurant', 'Restaurant'),
        ('citizen', 'Citizen'),
        ('ngo', 'NGO'),
        ('driver', 'Driver')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, max=100)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        User = User.get_by_username(username.data)
        if User:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        User = User.get_by_email(email.data)
        if User:
            raise ValidationError('Email already registered. Please choose a different one.')

class DonationForm(FlaskForm):
    food_type = SelectField('Food Type', choices=[
        ('prepared_food', 'Prepared Food'),
        ('raw_ingredients', 'Raw Ingredients'),
        ('packaged_food', 'Packaged Food'),
        ('beverages', 'Beverages'),
        ('bakery_items', 'Bakery Items'),
        ('dairy_products', 'Dairy Products'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity (approximate servings)', validators=[
        DataRequired(), 
        NumberRange(min=1, max=1000, message='Quantity must be between 1 and 1000')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=10, max=500, message='Description must be between 10 and 500 characters')
    ])
    location = StringField('Pickup Location', validators=[
        DataRequired(), 
        Length(min=5, max=200, message='Location must be between 5 and 200 characters')
    ])
    contact_phone = StringField('Contact Phone', validators=[
        DataRequired(), 
        Length(min=10, max=15, message='Please provide a valid phone number')
    ])
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError

# ⚠ Import your User model here if you have it
# from yourapp.models import User  

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[Length(max=15)])
    role = SelectField('Role', choices=[
        ('restaurant', 'Restaurant'),
        ('citizen', 'Citizen'),
        ('ngo', 'NGO'),
        ('driver', 'Driver')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, max=100)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        # ⚠ Requires a User model with get_by_username method
        user = None  # replace with: User.get_by_username(username.data)
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        # ⚠ Requires a User model with get_by_email method
        user = None  # replace with: User.get_by_email(email.data)
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class DonationForm(FlaskForm):
    food_type = SelectField('Food Type', choices=[
        ('prepared_food', 'Prepared Food'),
        ('raw_ingredients', 'Raw Ingredients'),
        ('packaged_food', 'Packaged Food'),
        ('beverages', 'Beverages'),
        ('bakery_items', 'Bakery Items'),
        ('dairy_products', 'Dairy Products'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity (approximate servings)', validators=[
        DataRequired(), 
        NumberRange(min=1, max=1000, message='Quantity must be between 1 and 1000')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=10, max=500, message='Description must be between 10 and 500 characters')
    ])
    location = StringField('Pickup Location', validators=[
        DataRequired(), 
        Length(min=5, max=200, message='Location must be between 5 and 200 characters')
    ])
    contact_phone = StringField('Contact Phone', validators=[
        DataRequired(), 
        Length(min=10, max=15, message='Please provide a valid phone number')
    ])
    submit = SubmitField('Donate')