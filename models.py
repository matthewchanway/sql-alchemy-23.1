from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    first_name = db.Column(db.String(50),
    nullable =False
    )

    last_name = db.Column(db.String(50),
    nullable =False
    )

    profile_url = db.Column(db.String(300),
    default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
    
    )


class Post(db.Model):

    __tablename__ = "posts"
    creator = db.relationship('User',backref='created_by')
    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    title = db.Column(db.String(50),
    nullable = False)

    content = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

