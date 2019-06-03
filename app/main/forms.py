from flask_wtf import FlaskForm
from app.models import User, Blog, Comment
from wtforms.validators import Required,Email,EqualTo
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, RadioField, TextAreaField, IntegerField, SelectField


class Blogform(FlaskForm):
    '''
    Blog post form.
    '''
    title = StringField('Title ')
    content = TextAreaField('Blog Content')
    submit = SubmitField('Publish')


class Commentform(FlaskForm):
    '''
    Comment form.
    '''
    name = StringField('Name', validators=[Required()])
    description = TextAreaField('Add comment', validators=[Required()])
    submit = SubmitField()


class UpdateForm(FlaskForm):
    title = StringField('Title for you Blog', validators=[Required()])
    content= TextAreaField('Blog Content', validators=[Required()])
    submit = SubmitField('Edit')
