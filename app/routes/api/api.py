from flask import Blueprint, request, jsonify, session
from app.models import db, Character
import requests
import json
from datetime import datetime

api_bp = Blueprint(
    'api', __name__, template_folder='templates', static_folder='static')


@api_bp.route('/characters', methods=['GET'])
def get_characters():
    if 'user_id' not in session:
        return jsonify({'message': 'Usuário não autenticado!'}), 401

    page = request.args.get('page', default=1, type=int)
    url = f'https://rickandmortyapi.com/api/character?page={page}'

    response = requests.get(url)
    data = response.json()

    if 'results' in data:
        characters = data['results']

        for char in characters:
            existing_character = Character.query.filter_by(
                character_id=char['id']).first()

            if not existing_character:
                created_datetime = datetime.fromisoformat(
                    char['created'].replace('Z', '+00:00'))

                new_character = Character(
                    character_id=char['id'],
                    name=char['name'],
                    status=char['status'],
                    species=char['species'],
                    gender=char['gender'],
                    type=char['type'],
                    origin=char['origin']['name'],
                    location=char['location']['name'],
                    episodes=json.dumps(char['episode']),
                    url=char['url'],
                    image=char['image'],
                    created=created_datetime
                )

                db.session.add(new_character)

        db.session.commit()

        character_summary = [
            {
                'id': char['id'],
                'name': char['name'],
                'status': char['status'],
                'species': char['species'],
                'gender': char['gender'],
                'type': char['type'],
                'origin': char['origin']['name'],
                'location': char['location']['name'],
                'episode_count': len(char['episode']),
                'url': char['url'],
                'image': char['image'],
                'created': char['created']
            }
            for char in characters
        ]

        return jsonify(character_summary), 200
    return jsonify({'message': 'Nenhum personagem encontrado!'}), 404
