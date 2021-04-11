"""Tables for KPGroupClass Launch Page and connection to database"""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, LargeBinary


db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///KPGroupClass', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """User stored in db."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key= True,)
    email = db.Column(db.String, unique = True)
    name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime,default=datetime.datetime.utcnow,)
   


    def __repr__(self):
        """show info about the registrant"""

        return f"<User ID={self.id} User name={self.name}, email = {self.email}, password = {self.password}>"


class Thoughts(db.Model):
    """thought processes stored in db."""
    __tablename__ = "thought"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key= True,)
    created_date = db.Column(db.DateTime,default=datetime.datetime.utcnow,)
    automatic_thought = db.Column(db.String)
    distortion = db.Column(db.String)
    distortion_plot = db.Column(db.Integer)
    more_realistic_thought = db.Column(db.String)
    author_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),)

    user_email = db.relationship('User', backref = 'Thoughts',)


    def __repr__(self):
        """show info about the registrant"""

        return f"< Thought ID={self.id}, email = {self.email}, automatic_thought = {self.automatic_thought},automatic_thought_plot = {self.automatic_thought_plot}, distortion = {self.distortion},distortion plot = {self.distortion_plot}, more_realistic_thought = {self.more_realistic_thought}, more_realistic_thought_plot = {self.more_realistic_thought_plot}>"




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()

    