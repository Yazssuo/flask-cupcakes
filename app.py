"""Flask app for Cupcakes"""
from flask import Flask, render_template, flash, redirect, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
        """Serializes to dictionary"""

        return {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image,
        }

@app.route('/api/cupcakes')
def get_cupcakes():
    """Gets all cupcakes from database"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cid>')
def get_cupcake(cid):
    """Gets a cupcake from database"""

    cupcake = Cupcake.query.get_or_404(cid)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    """Adds a cupcake to database"""

    c_data = request.get_json()
    
    cupcake = Cupcake(flavor=c_data.get('flavor'), size=c_data.get('size'), rating=c_data.get('rating'), image=c_data.get('image'))
    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cid>', methods=["PATCH"])
def update_cupcake(cid):
    """Updates a cupcake from database"""

    data = request.get_json()
    cupcake = Cupcake.query.get_or_404(cid)
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cid>', methods=["DELETE"])
def del_cupcake(cid):
    """Deletes a cupcake from database"""

    cupcake = Cupcake.query.get_or_404(cid)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route('/')
def homepage():
    """Renders homepage"""

    return render_template('index.html')