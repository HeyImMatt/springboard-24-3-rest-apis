"""Flask Cupcakes Exercise"""

from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bakery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'cupcakes1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    return {
      "id": cupcake.id,
      "flavor": cupcake.flavor,
      "size": cupcake.size,
      "rating": cupcake.rating,
      "image": cupcake.image
    }

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    """Get cupcakes route"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_single_cupcake(id):
    """Get cupcakes route"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)
