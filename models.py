from flask_sqlalchemy import SQLAlchemy
from flask_session import SqlAlchemySessionInterface
from app.extensions import db, sess, migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

    sess.init_app(app)
    SqlAlchemySessionInterface(app, db, "sessions", "sess_")

# MAIN TABLES

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
    username = db.Column(db.String(20), 
                        nullable=False, 
                        unique=True)
    password = db.Column(db.Text, 
                        nullable=False)
    email = db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    first_name = db.Column(db.String(30),
                        nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)
    account_type = db.Column(db.String(30),
                        nullable=False)
    last_login = db.Column(db.DateTime, 
                        server_default=db.func.now(), 
                        server_onupdate=db.func.now())

    work = db.relationship('UserWork', secondary="user_work_stats", backref='user', cascade="all,delete")

    students = db.relationship('Student', backref='users', cascade="all,delete")


    # start_register
    @classmethod
    def register(cls, first_name, last_name, email, username, password, account_type):
        """Register user w/hashed password & return user."""

        hashed = Bcrypt.generate_password_hash(cls, password, 14)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_utf8, account_type=account_type)
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

    @classmethod
    def reset_pass(cls, username, current_password, new_password):
        """Register user w/hashed password & return user."""

        u = User.query.filter_by(username=username).first()

        if u and Bcrypt.check_password_hash(cls, u.password, current_password):
            hashed = Bcrypt.generate_password_hash(cls, new_password, 14)
                # turn bytestring into normal (unicode utf8) string
            hashed_utf8 = hashed.decode("utf8")

            u.password = hashed_utf8

            db.session.add(u)

            db.session.commit()
                # return user instance
            return u
        else:
            return False


    @classmethod
    def delete_user(cls, username, password):
        """Register user w/hashed password & return user."""

        u = User.query.filter_by(username=username).first()

        userStats = u.tajweed_rule

        if u and Bcrypt.check_password_hash(cls, u.password, password):
            for rule in userStats:
                deletedStat = TajweedRules.query.filter_by(id=rule.id).delete()

            deleted =  User.query.filter_by(username=username).delete()
         
            db.session.commit()
            print('##########################################deleted', deleted)

            
            return 'deleted'
        else:
            return False

class TajweedRules(db.Model):
    """Tajweed Rules."""

    __tablename__ = "tajweed_rules"

    id = db.Column(db.Integer, 
                    primary_key=True)
    code = db.Column(db.Text, 
                    nullable=False,
                    unique=True)
    name = db.Column(db.Text, 
                    nullable=True)
    summary = db.Column(db.Text, 
                    nullable=True)
    details = db.Column(db.Text, 
                    nullable=True)
    example = db.Column(db.Text, 
                    nullable=True)
    audio = db.Column(db.Text, 
                    nullable=True)
    with_exercise = db.Column(db.Boolean,
                    default=True)


class UserWork(db.Model):
    """User practice and tests"""

    __tablename__="user_work"

    id = db.Column(db.Integer, 
                primary_key=True)
    rule = db.Column(db.Text, nullable=False)
    practice = db.relationship('Practice', backref='user_work', cascade="all,delete")
    practice_ayah_count = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    test = db.relationship('Test', backref='user_work', cascade="all,delete")
    test_ayah_count = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    total_correct = db.Column(db.Integer,
                    nullable=False,
                    default=0)
    total_out_of = db.Column(db.Integer,
                    nullable=False,
                    default=0)

    user_ref = db.relationship('User', secondary="user_work_stats", backref='user_work', cascade="all,delete")



class UserWorkStats(db.Model):
    """User Work Stats"""

    __tablename__ = "user_work_stats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    work_id = db.Column(db.Integer, db.ForeignKey('user_work.id', ondelete="cascade"))

      
class Practice(db.Model):
    """Practice Stat"""

    __tablename__ = "practice"

    id = db.Column(db.Integer, primary_key=True)
    practice_date = db.Column(db.DateTime, 
                nullable=False)
    ayah_count = db.Column(db.Integer,
                nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('user_work.id', ondelete="cascade"))
    user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

class Test(db.Model):
    """Test Stats"""

    __tablename__= "test"

    id = db.Column(db.Integer, primary_key=True)
    test_date = db.Column(db.DateTime, 
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
    rule_id = db.Column(db.Integer, db.ForeignKey('user_work.id', ondelete="cascade"))                    
    user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

class Student(db.Model):
    """Student Info"""

    __tablename__= "student"

    student_username = db.Column(db.String(20), 
                        primary_key=True,
                        nullable=False)
    student_email = db.Column(db.String(50),
                        nullable=False)
    student_firstName = db.Column(db.String(30),
                        nullable=False)
    student_lastName = db.Column(db.String(30),
                        nullable=False)
    teacher = db.Column(db.String(20), db.ForeignKey('users.username', ondelete="cascade"))
