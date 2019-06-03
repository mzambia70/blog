from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):
    '''
    Class blog that hold all blog data
    '''
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(), index=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.String)
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')


    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return blogs

    def get_post_comments(self):
        return Comment.query.filter_by(blog_id=self.id)

    def __repr__(self):
        return f'Blog {self.content}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    description = db.Column(db.Text)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
      '''
      Deletes and commits comment instance from database
      db.session.add(comment)
      db.session.commit()
      '''
      db.session.delete(self)
      db.session.commit()

    def __repr__(self):
      return f"Comment('{self.comment}')"


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

