from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
)
from src.database import db, User
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from flasgger import swag_from
from src.forms import RegistrationForm, LoginForm,  PasswordresetForm
from src.instance import bcrypt
from flask_bcrypt import generate_password_hash


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    form = RegistrationForm()
    # get request body
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    confirm_password = request.json["confirm_password"]

    # checks if form validation is successfull
    if form.validate():
        form.username.data = username
        form.email.data = email
        form.password.data = password
        form.confirm_password.data = confirm_password

        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        user = User(username=username, email=email, password=password)
        user.create_password_hash(password)
        print(user.password)
        db.session.add(user)
        db.session.commit()

        return (
            jsonify(
                {"message": "User created successfully ", "user": {
                    "username": username, "email": email}}
            )), HTTP_201_CREATED
    else:
        return jsonify({
            'error': form.errors
        }), HTTP_400_BAD_REQUEST


@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():

    email = request.json["email"]
    password = request.json["password"]

    # To check if user exist in db
    # first filter by the email if the user with that email already exist
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({
            "error": "This user does not exist try registering to get access"
        }), HTTP_400_BAD_REQUEST
        
    is_pass_correct = bcrypt.check_password_hash(user.password, password)
        
    # if user exists and passwords matches hashed password
    if user and is_pass_correct:

        # if user and password is correct

        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return (
            jsonify(
                {
                    "user": {
                        "refresh": refresh,
                        "access": access,
                        "username": user.username,
                        "email": user.email,
                    }
                }
            ),
            HTTP_200_OK,
        )

    return jsonify({
        "error": "Invalid password for this account, passwords might be case sensitive"
    }),HTTP_401_UNAUTHORIZED


@auth.post("/passwordreset")
@swag_from("./docs/auth/password_reset.yaml")
def passwordreset():
    email = request.json["email"]
    password = request.json["password"]
    confirm_password = request.json["confirm_password"]

    form = PasswordresetForm()

    form.email.data = email
    form.password.data = password
    form.confirm_password.data = confirm_password

    email = form.email.data
    password = form.password.data
    confirm_password = form.confirm_password.data

    if form.validate():
        user = User.query.filter_by(email=email).first()
        if user:
            new_password = generate_password_hash(password)
            user.password = new_password
            db.session.commit()
            return (
                jsonify({
                    "message": "password changed successfully"
                })
            ), HTTP_200_OK
    return (
        jsonify({
            "error": form.errors
        })
    ), HTTP_400_BAD_REQUEST


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({"username": user.username, "email": user.email}), HTTP_200_OK


@auth.get("/token/refresh")
@jwt_required(refresh=True)
@swag_from("./docs/auth/token_refresh.yaml")
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK
