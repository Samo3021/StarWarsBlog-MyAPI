from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    favChild = db.relationship('Favorites', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "userid": self.userid,
            "name":self.name,
            "lastname":self.lastname,
            "email":self.email,
            "favChild": list(map(lambda x: x.serialize(), self.favChild))
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(80), )
    skin_color = db.Column(db.String(80))
    eye_color = db.Column(db.String(80))
    hair_color = db.Column(db.String(80))
    height = db.Column(db.String(80))
    homeworld = db.Column(db.String(80))
    def __repr__(self):
        return '<People %r>' % self.Full_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "homeworld": self.homeworld
            # do not serialize the password, its a security breach
        }        
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(80), )
    gravity = db.Column(db.String(80))
    orbital_period = db.Column(db.String(80))
    population = db.Column(db.String(80))
    rotation_period = db.Column(db.String(80))
    terrain = db.Column(db.String(80))
    def __repr__(self):
        return '<Planets %r>' % self.Full_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }                
class Favorites(db.Model):
    idfav = db.Column(db.Integer, primary_key=True)
    user_userid  = db.Column(db.Integer, db.ForeignKey("user.userid"))
    name = db.Column(db.String(120),)
    object_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Favorites %r>' % self.idfav

    def serialize(self):
        return {
            "idfav": self.idfav,
            "user_userid": self.user_userid,
            "name":self.name,
            "object_id":self. object_id
            
            # do not serialize the password, its a security breach
        }                        