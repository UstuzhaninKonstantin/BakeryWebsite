from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    number = PasswordField('Номер карты', validators=[DataRequired()])
    time1 = IntegerField('Срок действия (ММ)', validators=[DataRequired()])
    time2 = IntegerField('Срок действия (ДД)', validators=[DataRequired()])
    name = StringField('Имя и фамилия владельца карты (Латиница)', validators=[DataRequired()])
    cvc = PasswordField('CVC/CVV', validators=[DataRequired()])
    city = StringField('Ваш город', validators=[DataRequired()])
    street = StringField('Улица, дом', validators=[DataRequired()])
    submit = SubmitField('Оплатить')
