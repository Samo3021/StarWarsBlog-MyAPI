"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():

    user_query = User.query.all()
    all_user = list(map(lambda x: x.serialize(), user_query))

    return jsonify(all_user), 200

@app.route('/people', methods=['GET'])
def get_people():

    people_query = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    
    person = People.query.get(people_id)
    
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets_query = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets_query))
    return jsonify(all_planets), 200
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):

    
    planet =  Planets.query.get(planets_id)
    
    return jsonify(planet.serialize()), 200
@app.route('/user/<int:userid>/favorites', methods=['GET'])
def get_userfav_id(userid):

    
    favorites =  Favorites.query.filter_by(user_userid = userid)
    results =list(map(lambda x: x.serialize(), favorites))
    return jsonify(results), 200

@app.route('/user/<int:userid>/favorites', methods=['POST'])
def add_favuser_id(userid):
    
    
    userfav = request.get_json()
    newfav= Favorites(name=userfav["name"], object_id=userfav["object_id"], user_userid = userid)
    db.session.add(newfav)
    db.session.commit()
    
    return jsonify(newfav.serialize()), 200
@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def del_favuser_id(favorite_id):
    
    
    delfav = Favorites.query.get(favorite_id)
    if delfav is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(delfav)
    db.session.commit()
    
    return jsonify("ak7s"), 200
        
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
