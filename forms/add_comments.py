from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LeaveComment(FlaskForm):
    text = TextAreaField('Комментарий', validators=[DataRequired()])
    rating = IntegerField('Ваша оценка от 1 до 5', validators=[DataRequired()])
    submit = SubmitField('Отправить')
