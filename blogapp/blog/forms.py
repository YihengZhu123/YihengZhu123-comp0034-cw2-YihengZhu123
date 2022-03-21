from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length


class BlogForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=3, max=100)])
    content = TextAreaField('Content',
                                validators=[InputRequired(),
                                            Length(max=200)])


class BlogCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired(),
                                             Length(min=3, max=100)])