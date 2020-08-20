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

@app.route('/')
def home_route():
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    """Get cupcakes route"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_single_cupcake(id):
    """Get single cupcake route"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    """Post cupcake route"""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    newCupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(newCupcake)
    db.session.commit()

    serialized = serialize_cupcake(newCupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def patch_cupcake(id):
    """Patch cupcake route"""

    cupcake = Cupcake.query.get_or_404(id)

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    cupcake.flavor = flavor if flavor else cupcake.flavor
    cupcake.size = size if size else cupcake.size
    cupcake.rating = rating if rating else cupcake.rating
    cupcake.image = image if image else cupcake.image

    # I think the loop works, but I get a rollback when committing
    # for k,v in request.json.items():
    #     if v and cupcake.__dict__[k]:
    #         cupcake.__dict__[k] = v 

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 200)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete cupcake route"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message="deleted"), 200)