from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

'''
1 - Creates an instance of this class. The first argument is the name of the application’s module or package.
 __name__ is a convenient shortcut for this that is appropriate for most cases. 
 This is needed so that Flask knows where to look for resources such as templates and static files.
'''

app = Flask(__name__)
# Reminder -> dictionary[key] = value
# 5 - SQLite is just a file that you can access with SQL. All SQLite requires is a simple Python library to work with.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # An sqlite database will be created in the same directory
db = SQLAlchemy(app)


# 6 - Define all the things we want to store in our database as Models
# 7 - The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance you have to create.
class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(150))

    # Overriding The repr method is used to get a string representation of a Python object. It is common to find
    # people using it when creating models for their flask app. With the repr method, you can make a query from the
    # database and print the result of the query. Instead of getting the location of the query object in memory,
    # the repr method provides a better representation of the result.
    def __repr__(self):
        return f'{self.name} - {self.description}'


# 2 - We then use the route() decorator to tell Flask what URL should trigger our function.
# app.route decorates a view function to register it with the given URL rule and options. Calls add_url_rule(),
# which has more details about the implementation.
# https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.route
@app.route('/')
# 3 - Method to be called when someone calls this route
# The function returns the message we want to display in the user’s browser. The default content type is HTML
# so HTML in the string will be rendered by the browser.
def index():
    return 'Hello World'


# 4 - Command Line: The flask command is installed by Flask, not your application; it must be told where to find your
# application in order to use it. The FLASK_APP environment variable is used to specify how to load the application.
#
# set FLASK_APP=app.py
# > flask run

# 5 - Create a new route
@app.route('/games')
def get_games():
    games = Games.query.all()

    # An empty list to hold all the data that will return from the query
    output = []
    for game in games:

        # game_data is a dictionary with two pairs of key/values
        game_data = {'name': game.name, 'description':game.description}
        # Each item in output will be a dictionary. Output is a list of dictionaries.
        output.append(game_data)
    return {'games': output}

# <id> is a hold value that will be substituted later
@app.route('/games/<id>')
def get_game(id):

    # get_or_404(ident, description=None) -> Like get() but aborts with 404 if not found instead of returning None
    game = Games.query.get_or_404(id)
    return {'name': game.name, 'description': game.description}

# 14 - A route for adding a game
# The methods parameter defaults to ["GET"]
@app.route('/games', methods=['POST'])
def add_drink():

    # Get the request data. When the method is called, it's going to pass the structure of what a game object should
    # look like.

    # An HTTP request is made by a client, to a named host, which is located on a server. The aim of the request is to
    # access a resource on the server. To make the request, the client uses components of a URL (Uniform Resource
    # Locator), which includes the information needed to access the resource.

    # request object -> https://flask.palletsprojects.com/en/2.0.x/api/?highlight=request#flask.request
    # To access incoming request data, you can use the global request object. Flask parses incoming request data for
    # you and gives you access to it through that global object.
    game = Games(name=request.json['name'], description=request.json['description'])
    db.session.add(game)
    db.session.commit()
    return {'id': game.id}

# 16 - Deleting a drink
@app.route('/games/<id>', methods=['DELETE'])
def delete_game(id):
    game = Games.query.get(id)
    if game is None:
        return 'Error: game not found'
    db.session.delete(game)
    db.session.commit()
    return {'message': f'{game.name} deleted'}

# 8 - In python shell:
# from app import db

# 9 - Creates all tables:
# db.create_all()

# 10 - Every time there's a need to use something from the application, it needs to be imported:
# from app import Games

# 11 - Create an object, still in the python shell:
# game = Games(name = 'game_name_here', description = 'description_here')

# 12 - To add to the table:
# db.session.add(game)

# 13 - Then:
# db.session.commit()

# 15 - Making a post request with Postman
