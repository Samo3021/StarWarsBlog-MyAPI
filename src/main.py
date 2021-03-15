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
import datetime
#from models import Person

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

#setuo del app
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)
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

@app.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_userfav_id():
    # selecionar Usuario
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    #como hacer la conexion
     
    #check de userio
    # user = userid
    
    #get all
    favorites =  Favorites.query.filter_by(user_userid = user.userid)
    results =list(map(lambda x: x.serialize(), favorites))
    return jsonify(results), 200

@app.route('/user/favorites', methods=['POST'])
@jwt_required()
def add_favuser_id():
    # selecionar Usuario
    email = get_jwt_identity()
    #ya se arreglo, lo que necesitabamos era poner el .first() al final para que seleccionara el usuario, no pense que era requerido pero parece que si.
    user = User.query.filter_by(email=email).first()
    print(email, user.userid)
    #add
    userfav = request.get_json()
    newfav= Favorites(name=userfav["name"], object_id=userfav["object_id"], user_userid=user.userid)
    db.session.add(newfav)
    db.session.commit()
    
    return jsonify(newfav.serialize()), 200
@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def del_favuser_id(favorite_id):
    # selecionar Usuario/es necesario jwt en delete?
    
    
    #del
    delfav = Favorites.query.get(favorite_id)
    if delfav is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(delfav)
    db.session.commit()
    
    return jsonify("ak7s"), 200

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        name = request.json.get("name", None)
        lastname = request.json.get("lastname", None)
        
        if not email:
            return jsonify({"msg":"Username is required"}), 400
        if not password:
            return jsonify({"msg":"Password is required"}), 400
        
        if not name:
            return jsonify({"msg":"name is required"}), 400
        if not lastname:
            return jsonify({"msg":"lastname is required"}), 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg":"Username already exists"}), 400
        
        user = User()
        user.email = email
        user.name = name
        user.lastname = lastname
        hashed_password = generate_password_hash(password)   

        print(password, hashed_password)
        
        user.password = hashed_password
        
        db.session.add(user)
        db.session.commit()
        return jsonify("registro correcto"), 200
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "Email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.email, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000,
            "activo": True  
        }
        
        return jsonify(data), 200
    
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200            
    return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200    
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
