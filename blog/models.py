from werkzeug.security import generate_password_hash, check_password_hash
from blog import login_manager
from flask_login import UserMixin
from datetime import datetime
from blog import db


class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False,
                           default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship(
        'Liked',
        foreign_keys='Liked.post_id',
        backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    liked = db.relationship(
        'Liked',
        foreign_keys='Liked.user_id',
        backref='user', lazy='dynamic')
    tagged_post = db.relationship(
        'Tagged',
        foreign_keys='Tagged.user_id',
        backref='user', lazy='dynamic')
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def like_post(self, post):
        if not self.has_liked(post):
            like = Liked(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked(post):
            Liked.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
    
    def has_liked(self, post):
        return Liked.query.filter(
            Liked.user_id == self.id,
            Liked.post_id == post.id).count() > 0

    def tag_post(self, post):
        if not self.has_tagged(post):
            tag = Tagged(user_id=self.id, post_id=post.id)
            db.session.add(tag)

    def untag_post(self, post):
        if self.has_tagged(post):
            Tagged.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
    
    def has_tagged(self, post):
        return Tagged.query.filter(
            Tagged.user_id == self.id,
            Tagged.post_id == post.id).count() >  0

    @property
    def view_tagged_posts(self):
        return Post.query.join(Tagged, Tagged.post_id == Post.id)\
            .filter(Tagged.user_id == self.id).all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'comment.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent = db.relationship(
        'Comment', backref='comment_parent', remote_side=id, lazy=True)

    def __repr__(self):
        return f"Post('{self.date}', '{self.content}')"

class Liked(db.Model):
    __tablename__='liked'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Tagged(db.Model):
    __tablename__='tagged'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
