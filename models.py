from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin

from peewee import *

DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):
    #  User accounts have an email address and a password
    # * User email addresses are unique
    email = CharField(unique=True)
    password = CharField(max_length=100)

    # * Logged in users see menu items for log out and to create a taco
    # * Logged out users see menu items to log in or sign up
    class Meta:
        db = DATABASE

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),  # * Passwords are hashed
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Taco(Model):
    # modelling a one-to-many relationship
    # * Tacos have a protein, a shell, a true/false for cheese, and a freeform area for extras
    protein = CharField()
    shell = CharField()
    cheese = BooleanField(default=False)
    extras = TextField(default='')
    user = ForeignKeyField(User)

    class Meta:
        db = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()