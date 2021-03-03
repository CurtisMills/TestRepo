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

    posts = Post.query.order_by(Post.date.desc()).limit(3)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/registration_complete")
def registration_complete():
    return render_template('registration_complete.html', title="Thanks for Registering")

@app.route("/allposts")
def allposts():
    sort_by = request.args.get('sortBy')
    posts = Post.query
    if sort_by=='ascending':
        posts = posts.order_by(Post.date.asc()).all()
    if sort_by=='descending':
        posts = posts.order_by(Post.date.desc()).all()
    
    return render_template('allposts.html', posts=posts)

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
    image_file = url_for('static', filename='/img')

    return render_template('post.html', post=post, comments=comments, form=form, image_file=image_file)


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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_term']
        search = "%{}%".format(search_value)
        results = Post.query.filter(Post.title.like(search)|Post.content.like(search)).all()
        return render_template('search.html', results=results, search=search_value)
    else: 
        return redirect('/home')

