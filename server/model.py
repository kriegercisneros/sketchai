from services import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

# from sqlalchemy_serializer import SerializerMixin

#new User class that inherits from db.Model 
#db.Model is a base class for all models from Flask-SQLAlchemy, where a model reps
#a table in a database
class User(db.Model):
    #below is a class-level variable that tells SQLAlchemy what the table name in db should be
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    #note the _ in front of the name of the column, this indicates it is not public
    _password_hash = db.Column(db.String)
    email = db.Column(db.String(80), unique=True, nullable=False)

    #the below decorator is from SQLALchemy that allows to define a method as if it were an 
    #instance property but also has some additional ORM-level expressions
    #using the hybrid_property has several benifits:
    #1. creates a neat API for getting and setting passwords
    #2. allows users to not directly manipulate the _password_hash
    @hybrid_property
    #the below is an instance method and returns the _password_hash value
    def password_hash(self):
        return self._password_hash
    
    #the below decorator defines the method as the setter for passowrd_hash property, meaning
    #if you assign a value to password_hash, this method will be invoked
    @password_hash.setter
    def password_hash(self, password):
        #note we need the encode and decode in python 3 due to special characters
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash=password_hash.decode('utf-8')

    #create an auth route using bcrypt
    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email
        }