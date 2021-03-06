from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(85), nullable= False)
    email = db.Column(db.String(255), unique=True, index= True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    password=db.Column(db.String(40),nullable=False)
    postman=db.relationship('Post',backref="postman")
    # blogs = db.relationship('Blog', backref ='user', passive_deletes=True,lazy = "dynamic")
    comments = db.relationship('Comment', backref ='user' , passive_deletes=True,  lazy ="dynamic")
   


    @property
    def password(self): 
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'
        

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title_blog = db.Column(db.String(255), index=True)
    description = db.Column(db.String(255), index=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
   
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.filter_by(id=id).all()
        return blogs
    @classmethod
    def get_all_blogs(cls):
        blogs = Blog.query.order_by('-id').all()
        return blogs
    def __repr__(self):
        return f'Blogs {self.blog_title}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id',ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comments(cls, blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return comments
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Comments: {self.comment}'
    
class posts(db.Model):
    id = db.Column(db.String, primary_key = True)
    blogs = db.Column(db.String(50) , primary_key = False)
    post = db.Column(db.String(50), primary_key = False)



class postss(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(25),nullable =False) 
    post = db.Column(db.String(50),nullable =False)
    poster=db.Column(db.Integer,db.ForeignKey('users.id'))
    poster=db.Column(db.Integer,db.ForeignKey('users.id'))

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    post=db.Column(db.String(700),nullable=False)
    poster=db.Column(db.Integer,db.ForeignKey('users.id'))

class Images(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    uploader_id=db.Column(db.Integer,db.ForeignKey('users.id'))


class House(db.Model):
    __tablename__='houses'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(2000),unique = True,index = True)
    house = db.Column(db.String(1000))
    time = db.Column(db.String(240))



    def save_house(self):
        db.session.add(self)
        db.session.commit()

    def delete_house(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_posts(cls,id):
        houses = House.query.filter_by(id=id).first()
        return houses

    def __repr__(self):
        return f'House {self.house}'

class Photo(db.Model):
    __tablename__='photos'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    description=db.Column(db.String(200))
    price=db.Column(db.String(200))
    photo_path=db.Column(db.String())

    def save_photo(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_photos(cls,id):
        photo = Photo.query.filter_by(id=id).first()
        return photo

    def __repr__(self):
        return f'Photo {self.photo}'

