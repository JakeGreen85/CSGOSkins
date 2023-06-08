from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
class AddCustomerForm(FlaskForm):
    user_name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    user_id = IntegerField('User ID',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Old Password', validators=[DataRequired()])
    newPassword = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class ChangeUsernameForm(FlaskForm):
    user_name = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Change Username')

class AddFundsForm(FlaskForm):
    customer = IntegerField('User ID', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Funds')