from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required

from schemas.recipe import RecipeSchema
from schemas.user import UserSchema
from webargs import fields
from webargs.flaskparser import use_kwargs

user_schema = UserSchema()

user_public_schema = UserSchema(exclude=('email',))
recipe_list_schema = RecipeSchema(many=True)


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        username = json_data.get('username')
        email = json_data.get('email')

        non_hash_password = json_data.get('password')

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        # password = hash_password(non_hash_password)

        # user = User(
        #     username=username,
        #     email=email,
        #     password=password
        # )

        user = User(**data)

        user.save()

        # data = {
        #     'id': user.id,
        #     'username': user.username,
        #     'email': user.email
        # }
        # return data, HTTPStatus.CREATED

        return user_schema.dump(user), HTTPStatus.CREATED


class UserRecipeListResource(Resource):
    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

        return recipe_list_schema.dump(recipes), HTTPStatus.OK


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
            # data = {

            #     'id': user.id,

            #     'username': user.username,

            #     'email': user.email,

            # }
            data = user_schema.dump(user)
        else:

            # data = {

            #     'id': user.id,

            #     'username': user.username,

            # }
            data = user_public_schema.dump(user)

        return data, HTTPStatus.OK


class MeResource(Resource):
    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        # data = {

        #     'id': user.id,
        #     'username': user.username,
        #     'email': user.email,
        # }
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user), HTTPStatus.OK
