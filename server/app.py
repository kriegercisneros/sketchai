from flask import make_response, jsonify, request, session
from services import app, db
from model import User

@app.route('/set-session')
def set_session():
    session.permanent = True
    session['key'] = 'value'
    return "Session set!"


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method =='GET':
        users =User.query.all()
        user_dict_list = [u.to_dict() for u in users]
        return make_response(jsonify(user_dict_list), 200)
    #this creates a new instance of the user class and posts to DB
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password_hash']
        user_exists = User.query.filter(User.email==email).first()
        if user_exists is not None:
            return jsonify({"error":"user already exists"}), 409
        data = request.get_json()
        try:
            user = User(email=email)
            user.password_hash = password 
            db.session.add(user)
            db.session.commit()
            session['user_id']= user.id
            return make_response(jsonify(user.to_dict(), {"message":"registered successfully"}), 201)
        except Exception as e:
            return make_response({"errors": [e.__str__()]}, 422)
# create a login route to see if a user exists
# with this one, use _password_hash as the key for the json data
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        jsoned_request = request.get_json()
        user = User.query.filter(User.email == jsoned_request['email']).first()
        if user and user.authenticate(jsoned_request["_password_hash"]):
            session["user_id"]= user.id
            return make_response(jsonify(user.to_dict(), {"message":"you are successfully logged in"}), 200)
        else:
            return make_response(jsonify({"login":"unauthorized"}), 401)
        
@app.route('/logout', methods = ['POST'])
def logout():
    if "user_id" in session:
        session.pop("user_id", None)
        return make_response(jsonify({"message":"logged out"}), 200)
    else:
        return make_response(jsonify({"message":"not logged in"}), 401)