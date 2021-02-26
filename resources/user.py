from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_optional,jwt_required


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')

        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        user = User(
            username=username,
            email=email,
            password=password
        )
        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.CREATED


class UserResource(Resource):
    
    # @jwt_optional This implies that the endpoint is accessible regardless of the procession of the token
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        # Also, the get_jwt_identity() function is provided to get the identity of a JWT in a protected endpoint.
        # This allows us to know who the authenticated users are
        # If it is found in the database, 
        # we will further check whether it matches the identity of the user ID in the JWT
        current_user = get_jwt_identity()

        if current_user == user.id:
            # it is private information and is only visible to the authenticated user 
            data = {

                'id': user.id,

                'username': user.username,

                'email': user.email,

            }
        else:
               
            data = {

                'id': user.id,

                'username': user.username,

            }

        return data, HTTPStatus.OK
    
class MeResource(Resource):
     # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        data = {

                'id': user.id,
                'username': user.username,
                'email': user.email,
        }
        return data, HTTPStatus.OK