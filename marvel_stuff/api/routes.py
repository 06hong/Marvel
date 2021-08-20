from flask import Blueprint, jsonify, request, url_for
from marvel_stuff.helpers import token_required
from marvel_stuff.models import Marvel, marvel_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/tester')
def getrando():
    return {'CodingTemple': 'rules'}


@api.route('/marvel', methods= ['POST'])
@token_required
def create_marvel(current_user_token):
    song = Marvel.query.get(id)
    name = request.json['name']
    powers = request.json['powers']
    traits = request.json['traits']
    user_token = current_user_token

    marvel= Marvel(name, powers, traits, user_token=user_token)

    db.session.add(marvel)
    db.session.commit()


    response = marvel_schema.dump(marvel)
    return jsonify(response)

@api.route('/marvel', methods= ['GET'])
@token_required
def get_marvel(current_user_token):
    owner = current_user_token.token
    marvel = Marvel.query.filter_by(user_token =owner).all()
    response = marvel_schema.dump(marvel)
    return jsonify(response)

@api.route('/marvel/<id>', methods= ['GET'])
@token_required
def get_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    if marvel:
        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'message':"That song does not exist pal.."})

@api.route('/marvel/<id>', methods= ['POST'])
@token_required
def create_marvel(current_user_token):
    song = Marvel.query.get(id)
    if song:
        song.name = request.json['name']
        song.powers = request.json['powers']
        song.traits = request.json['traits']
        song.user_token = current_user_token
    
    db.session.commit()


    response = marvel_schema.dump(marvel)
    return jsonify(response)
else:
    jsonify({'message': 'That song does not exist pal'})

@api.route('/marvel/<id>', methods= ['GET'])
@token_required
def get_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    if marvel:
        db.session.delete(marvel)
        db.session.commit()
        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'message':"That song does not exist pal.."})



