from flask import Blueprint,request,jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from src.database import db, User
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required,get_jwt_identity, create_access_token, create_refresh_token
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from("./docs/auth/register.yaml")
def register():
    username=request.json['username']
    email= request.json['email']
    password = request.json['password']


    if len(password) < 6:
        return jsonify({
        'error':"Password is too short "
        }), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({
        'error':"Username is too short"
        }), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({
            'error':"Username should be alphanumeric, also no spaces"
        }), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({
            'error': "Email is not valid"
        }),HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error':"Email is taken"
        }), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            'error':"Username is taken"
        }), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message':"User created",
        'user': {
            'username':username,
            'email':email
        }
    }), HTTP_201_CREATED

    
@auth.post('/login')
@swag_from("./docs/auth/login.yaml")
def login():
    #variables to get user details from json
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    # To check if user exist in db
    #first filter by the email if the user with that email already exist
    user= User.query.filter_by(email=email).first()

    #if user exists
    if user:
        # check if user password is correct
        is_pass_correct = check_password_hash(user.password, password)
        
       

        # if user password is correct 
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                    'refresh':refresh,
                    'access' : access,
                    'username': user.username,
                    'email': user.email
                }
            }),HTTP_200_OK

    return jsonify({
        'error':"Wrong credentials"
    }), HTTP_401_UNAUTHORIZED
 
@auth.post('/forgotpassword')
@swag_from("./docs/auth/forgotpassword.yaml")
def forgotpassword():
    email = request.json['email']
    password = request.json['password']
    
    pwd_hash = generate_password_hash(password)
    
    #check if email exist in db
    if not validators.email(email):
        return jsonify({
            'err':"This email is not valid"
        }), HTTP_400_BAD_REQUEST
        
    user = User.query.filter_by(email=email).first()
    
    
    if user is None:
        return jsonify({
            'err':"This user does not exist"
        }), HTTP_400_BAD_REQUEST
    elif user:
        # filter by the user and change the password of the user 
        user.password = pwd_hash
        db.session.commit()
        
        return jsonify({
            'message':"password changed successfully"
        }), HTTP_200_OK

               

@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    
    return jsonify({
            'username': user.username,
            'email': user.email
   }), HTTP_200_OK



@auth.get ('/token/refresh')
@jwt_required(refresh=True)
@swag_from("./docs/auth/token_refresh.yaml")
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }), HTTP_200_OK

