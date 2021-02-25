# CREATING A USER AND A RECIPE
from app import *

from models.user import User

from models.recipe import Recipe

app = create_app()

with app.app_context():
    user = User(username='peter', email='peter@gmail.com', password='Quien')
    
    db.session.add(user)
    db.session.commit()
    
    encebollado = Recipe(name='Encebollado', description='El encebollado es un plato típico ecuatoriano originario de la región costa', num_of_servings=1, cook_time=30, directions='hay que conseguir albacora', user_id=user.id)
    lasagnia = Recipe(name='lasaña', description='La lasaña es un tipo de pasta que se sirve en láminas para denominarse lasaña ha de llevar ', num_of_servings=1, cook_time=30, directions='Las laminas paso 1', user_id=user.id)

    db.session.add(encebollado)
    db.session.add(lasagnia)
    db.session.commit()
    
    user = User.query.filter_by(username='peter').first()
    
    for recipe in user.recipes:
        print('{} recipe made by {} can serve {} people.'.format(recipe.name, recipe.user.username, recipe.num_of_servings))
