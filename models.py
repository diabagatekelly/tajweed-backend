from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MAIN TABLES

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
    username = db.Column(db.String(20), 
                        nullable=False)
    password = db.Column(db.Text, 
                        nullable=False)
    email = db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    first_name = db.Column(db.String(30),
                        nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)
    last_login = db.Column(db.DateTime, 
                        server_default=db.func.now(), 
                        server_onupdate=db.func.now())

    tajweed_rule = db.relationship('TajweedRules', secondary="user_tajweed_stats", backref='user')

    # start_register
    @classmethod
    def register(cls, first_name, last_name, email, username, password):
        """Register user w/hashed password & return user."""

        hashed = Bcrypt.generate_password_hash(cls, password, 14)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_utf8)
        db.session.add(user)
        return user
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and Bcrypt.check_password_hash(cls, u.password, password):
            u.last_login = db.func.now()

            db.session.add(u)

            db.session.commit()
            # return user instance
            return u
        else:
            return False
    # end_authenticate    


class TajweedRules(db.Model):
    """Tajweed Rules."""

    __tablename__ = "tajweed_rules"

    code = db.Column(db.Text, 
                    primary_key=True)
    name = db.Column(db.Text,
                    nullable=False)
    last_practice = db.Column(db.DateTime, 
                    nullable=True)
    practice_ayah_count = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    last_test = db.Column(db.DateTime, 
                    nullable=True)
    test_ayah_count = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    test_score_correct = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    test_out_of_count = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    test_score_composite = db.Column(db.Text,
                        nullable=False,
                        default='0/0')
    total_correct = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    total_out_of = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    
    
    user_rule = db.relationship('User', secondary="user_tajweed_stats", backref='tajweed_rules')



class UserTajweedStats(db.Model):
    """User_Tajweed Link"""

    __tablename__ = "user_tajweed_stats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rule_code = db.Column(db.Text, db.ForeignKey('tajweed_rules.code'))