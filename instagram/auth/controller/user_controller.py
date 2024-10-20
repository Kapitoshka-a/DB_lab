import pymysql
from flask import Blueprint, request, jsonify

from config.config import Config
from instagram.auth.dao.user_dao import UserDAO
from instagram.auth.dto.user_dto import UserDTO, UserStoryDTO, HashtagDTO
from instagram.auth.service.user_service import UserService

user_bp = Blueprint('user', __name__)

config = Config()
db = pymysql.connect(host=config.DB_HOST,
                     user=config.DB_USER,
                     password=config.DB_PASSWORD,
                     database=config.DB_NAME)


# Ініціалізація сервісу користувачів
user_dao = UserDAO(db)
user_service = UserService(user_dao)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    user_dtos = [UserDTO(user[0], user[1], user[2]).to_dict() for user in users]
    return jsonify(user_dtos)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    user_service.create_user(username, email, password)
    return jsonify({'message': 'User created successfully!'}), 201


@user_bp.route('/users/<int:user_id>/stories', methods=['GET'])
def get_user_stories(user_id):
    stories = user_service.get_user_stories(user_id)
    user_story_dtos = [UserStoryDTO(story[0], story[1], story[2], story[3], story[4], story[5]).to_dict() for story in
                       stories]
    return jsonify(user_story_dtos)


@user_bp.route('/users/<int:user_id>/hashtags', methods=['GET'])
def get_user_hashtags(user_id):
    hashtags = user_service.get_hashtags_from_user_stories(user_id)
    hashtag_dtos = [HashtagDTO(hashtag[0], hashtag[1], hashtag[2]).to_dict() for hashtag in hashtags]
    return jsonify(hashtag_dtos)


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user_service.update_user(user_id, username=username, email=email, password=password)
    return jsonify({'message': 'User updated successfully!'})


@user_bp.route('/users/<int:user_id>/stories/<int:story_id>', methods=['DELETE'])
def delete_story(user_id, story_id):
    user_service.delete_story(user_id, story_id)
    return jsonify({'message': 'Story deleted successfully!'}), 204
