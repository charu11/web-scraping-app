from scraping import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# define the User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        if bcrypt.check_password_hash(self.password, attempted_password):
            return True

# define the details table
class Details(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    state = db.Column(db.String(30), nullable=False, unique=False)
    address = db.Column(db.String(30), nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=True, default=0)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))





