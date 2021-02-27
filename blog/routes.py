from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, CommentForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from markupsafe import escape


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/registration_complete")
def registration_complete():
    return render_template('registration_complete.html', title="Thanks for Registering")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful.')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        flash('Invalid email address or password.')
        return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('logout_complete'))


@app.route("/logout_complete")
def logout_complete():
    return render_template('logout_complete.html', title="Logout Successful")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    form = CommentForm()

    return render_template('post.html', post=post, comments=comments, form=form)


@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data,
                               post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(f'/post/{post.id}')

    comments = Comment.query.filter(Comment.post_id == post.id)
    return render_template('post.html', post=post, comments=comments, form=form)

@app.route("/search")
def search():

    keyword = escape(request.form.get("keyword"))
    posts = Post.query.filter((Post.title.like(f'%{keyword}%'))).all()

    if posts is None:
        return render_template('home.html')

    return render_template('search.html', title='Search', posts=posts)

@app.route('/like/<int:post_id>/<action>')
@login_required
def post_like(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/tag/<int:post_id>/<action>')
@login_required
def post_tag(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'tag':
        current_user.tag_post(post)
        db.session.commit()
    if action == 'untag':
        current_user.untag_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/tagged_posts')
@login_required
def view_tagged():
    return render_template('tagged_post.html', tags=current_user.view_tagged_posts)
