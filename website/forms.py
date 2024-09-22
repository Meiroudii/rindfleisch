from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter your password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm new password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_image = FileField('Product Image', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')
    description = StringField('Description', validators=[DataRequired()])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')

class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

    update = SubmitField('Update Status')

class UserRoleForm(FlaskForm):
    is_admin = BooleanField('Flash Sale')
    update_role = SubmitField('Update Role')
