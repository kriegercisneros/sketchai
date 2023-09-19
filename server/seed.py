from services import db,app
from model import User

with app.app_context():
    print("creating users")
    db.create_all()
    # User.query.delete()
    try:
        new_user = User(email="test@test.com", password_hash="test")
        
        db.session.add(new_user)
        db.session.commit()
        print("user added successfully")
    except Exception as e:
        db.session.rollback()
        print(f"an error occurred: {e}")