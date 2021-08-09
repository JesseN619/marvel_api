from flask import Blueprint, request, jsonify
from marvel_app.helpers import token_required
from marvel_app.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 'hello', 'another_value': 'world'}

# CREATE
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    character = Character(name, description, comics_appeared_in, super_power, user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# RETRIEVE ALL CHARACTERS
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# RETRIEVE SINGLE CHARACTER
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

# UPDATE
@api.route('/characters/<id>', methods = ['POST'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)
    if character:
        character.name = request.json['name']
        character.description = request.json['description']
        character.comics_appeared_in = request.json['comics_appeared_in']
        character.super_power = request.json['super_power']
        character.user_token = current_user_token.token
        
        db.session.commit()

        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That character does not exist!'})

#DELETE
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    if character:
        db.session.delete(character)
        db.session.commit()

        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That character does not exist!'})