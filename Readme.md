para los colores
https://coolors.co/b8336a-c695be-726da8-7d8cc4-a0d2db-b2b1d6-c490d1

# Use the following command in the Terminal to initialize our database. This will create a migration repository:
flask db init

# run the flask db migrate command to create the database and tables. There is no need for us to use SQL here
flask db migrate

# which will upgrade our database to conform with the latest specification in our models
flask db upgrade