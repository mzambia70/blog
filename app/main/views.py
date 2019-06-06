from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from ..models import User,Blog,Comment
import os
import requests
import json
# from flask.views import View, MethodView
from .. import db, photos
from .forms import Blogform,Commentform,UpdateForm
from . import main
from datetime import datetime



#views
@main.route ('/')
def index():
    '''
    View root page funct that returns the index page and its data
    '''
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()

    return render_template('index.html', random = random)


@main.route('/posts')
def blog():
    blogs = Blog.query.order_by(Blog.date_posted.desc())
    return render_template('posts.html', blogs=blogs)


@main.route('/blogs/<int:blog_id>',methods = ["GET","POST"])
def view_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()  
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()

    form = Commentform()
    if form.validate_on_submit():
        name = form.name.data
        content = form.content.data
        new_comment = Comment(name=name, content=content,blog_id=blog.id)
        new_comment.save_comment()
        return redirect(url_for('main.view_blog', blog_id=blog.id))
    comments = Comment.query.filter_by(blog_id=blog.id)

    return render_template("blogs.html", form=form, blog=blog, comments=comments, random = random)

@main.route('/blogs/new/', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = Blogform()
    if form.validate_on_submit():
        content = form.content.data
        title = form.title.data
        owner_id = current_user
        date_posted = str(datetime.now())
        print(current_user._get_current_object().id)
        new_blog = Blog(owner_id=current_user._get_current_object().id, title=title, content=content,
                          date_posted=date_posted)
        db.session.add(new_blog)
        db.session.commit()
        # flash('New blog post created','success')

        return redirect(url_for('main.blog'))
    return render_template('new.html', form=form)


@main.route("/delete/<blog_id>",methods = ['GET','POST'])
def delete(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.blog'))


@main.route("/update/<blog_id>", methods= ['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    form = UpdateForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        return redirect(url_for('main.blog'))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content


    return render_template('new.html', form=form)


@main.route('/<int:blog_id>/delete comments')
@login_required
def delete_comment(blog_id):
    comment = Comment.query.filter_by(blog_id=blog_id).first()
    blog_id = comment.blog_id

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.view_blog', blog_id=blog_id))




@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

