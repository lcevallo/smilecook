from flask import request
from flask_restful import Resource
from http import HTTPStatus

from marshmallow import ValidationError

from models.recipe import Recipe
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()

recipe_list_schema = RecipeSchema(many=True)


class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()

        return recipe_list_schema.dump(recipes), HTTPStatus.OK

        # data = []
        # for recipe in recipes:
        #     data.append(recipe.data)

        # return {'data': data}, HTTPStatus.OK

    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()
        try:
            data = recipe_schema.load(data=json_data)

            recipe = Recipe(**data)

            recipe.user_id = current_user

            recipe.save()

            return recipe_schema.dump(recipe), HTTPStatus.CREATED

        except ValidationError as err:
            err.messages  # => {'email': ['"foo" is not a valid email address.']}
            valid_data = err.valid_data  # => {'name': 'John'}
            return {'message': "Validation errors", 'errors': err.messages}, HTTPStatus.BAD_REQUEST

        # recipe = Recipe(
        #     name=json_data['name'],
        #     description=json_data['description'],
        #     num_of_servings=json_data['num_of_servings'],
        #     cook_time=json_data['cook_time'],
        #     directions=json_data['directions'],
        #     user_id=current_user
        # )
        # recipe.save()

        # return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):

    # decorator specifies that the JWT is optional
    @jwt_optional
    def get(self, recipe_id):
        # recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True),
        # None)
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # we will further check whether it matches the identity of the user ID in the JWT
        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe.data, HTTPStatus.OK

    @jwt_required
    def patch(self, recipe_id):
        json_data = request.get_json()
        try:
            data = recipe_schema.load(data=json_data, partial=('name',))

            recipe = Recipe.get_by_id(recipe_id=recipe_id)

            if recipe is None:
                return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

            current_user = get_jwt_identity()

            if current_user != recipe.user_id:
                return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

            recipe.name = data.get('name') or recipe.name

            recipe.description = data.get('description') or recipe.description

            recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings

            recipe.cook_time = data.get('cook_time') or recipe.cook_time

            recipe.directions = data.get('directions') or recipe.directions

            recipe.save()

            return recipe_schema.dump(recipe), HTTPStatus.OK

        except ValidationError as err:
            err.messages  # => {'email': ['"foo" is not a valid email address.']}
            valid_data = err.valid_data  # => {'name': 'John'}
            return {'message': 'Validation errors', 'errors': err.messages}, HTTPStatus.BAD_REQUEST

    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def put(self, recipe_id):
        json_data = request.get_json()

        # recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # we will further check whether it matches the identity of the user ID in the JWT
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.name = json_data['name']
        recipe.description = json_data['description']
        recipe.num_of_servings = json_data['num_of_servings']
        recipe.cook_time = json_data['cook_time']
        recipe.directions = json_data['directions']

        recipe.save()

        return recipe.data, HTTPStatus.OK

    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def delete(self, recipe_id):
        # recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # we will further check whether it matches the identity of the user ID in the JWT
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        # recipe_list.remove(recipe)
        recipe.delete()

        return {}, HTTPStatus.NO_CONTENT


class RecipePublishResource(Resource):
    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True

        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

    # decorator here says that the method can only be invoked after the user has logged in
    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = False

        recipe.save()

        return {}, HTTPStatus.NO_CONTENT
