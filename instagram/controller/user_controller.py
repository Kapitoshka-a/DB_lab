from flask import Blueprint, request, jsonify
from instagram.dao.user_dao import UserDAO
from instagram.dto.user_dto import UserDTO, UserStoryDTO, HashtagDTO
from instagram.service.user_service import UserService
user_bp = Blueprint('user', __name__)


user_dao = UserDAO()
user_service = UserService(user_dao)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: User ID
              username:
                type: string
                description: Username
              email:
                type: string
                description: User email
        examples:
          application/json:
            - id: 1
              username: "john_doe"
              email: "john@example.com"
            - id: 2
              username: "jane_smith"
              email: "jane@example.com"
    """
    users = user_service.get_all_users()
    user_dtos = [UserDTO(user[0], user[1], user[2]).to_dict() for user in users]
    return jsonify(user_dtos)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              description: Unique username
              example: "john_doe"
            email:
              type: string
              format: email
              description: User email address
              example: "john@example.com"
            password:
              type: string
              format: password
              description: User password
              example: "securepassword123"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User created successfully!"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username already exists"
    """
    data = request.json
    username = str(data['username'])
    email = str(data['email'])
    password = str(data['password'])
    user_service.create_user(username, email, password)
    return jsonify({'message': 'User created successfully!'}), 201

@user_bp.route('/users/stories', methods=['GET'])
def get_user_stories():
    """
    Get stories for all users
    ---
    tags:
      - Users
      - Stories
    responses:
      200:
        description: Stories grouped by user
        schema:
          type: array
          items:
            type: array
            items:
              type: object
              properties:
                id:
                  type: integer
                  description: Story ID
                user_id:
                  type: integer
                  description: User ID who created the story
                content:
                  type: string
                  description: Story content
                created_at:
                  type: string
                  format: datetime
                  description: Story creation timestamp
        examples:
          application/json:
            - - id: 1
                user_id: 1
                content: "My first story"
                created_at: "2023-01-01T10:00:00Z"
            - - id: 2
                user_id: 2
                content: "Another story"
                created_at: "2023-01-01T11:00:00Z"
    """
    ids = user_service.get_users_ids()
    user_ids = [item[0] for item in ids]
    stories_by_user = []
    for user_id in user_ids:
        stories = user_service.get_user_stories(user_id)
        user_story_dtos = [UserStoryDTO(*story).to_dict() for story in stories]
        stories_by_user.append(user_story_dtos)

    return jsonify(stories_by_user)

@user_bp.route('/users/hashtags', methods=['GET'])
def get_user_hashtags():
    """
    Get hashtags from user stories
    ---
    tags:
      - Users
      - Hashtags
    responses:
      200:
        description: List of hashtags from user stories
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Hashtag ID
              tag:
                type: string
                description: Hashtag text
              story_id:
                type: integer
                description: Associated story ID
              count:
                type: integer
                description: Usage count
        examples:
          application/json:
            - id: 1
              tag: "travel"
              story_id: 1
              count: 5
            - id: 2
              tag: "food"
              story_id: 2
              count: 3
    """
    hashtags = user_service.get_hashtags_from_user_stories()
    hashtag_dtos = [HashtagDTO(hashtag[0], hashtag[1], hashtag[2], hashtag[3]).to_dict() for hashtag in hashtags]
    return jsonify(hashtag_dtos)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user information
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: New username
              example: "john_doe_updated"
            email:
              type: string
              format: email
              description: New email address
              example: "john.updated@example.com"
            password:
              type: string
              format: password
              description: New password
              example: "newpassword123"
    responses:
      200:
        description: User updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User updated successfully!"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user_service.update_user(user_id, username=username, email=email, password=password)
    return jsonify({'message': 'User updated successfully!'})

@user_bp.route('/users/<int:user_id>/stories/<int:story_id>', methods=['DELETE'])
def delete_story(user_id, story_id):
    """
    Delete a specific story
    ---
    tags:
      - Users
      - Stories
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID who owns the story
      - name: story_id
        in: path
        type: integer
        required: true
        description: Story ID to delete
    responses:
      204:
        description: Story deleted successfully
      404:
        description: Story not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Story not found"
      403:
        description: User not authorized to delete this story
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not authorized to delete this story"
    """
    user_service.delete_story(user_id, story_id)
    return jsonify({'message': 'Story deleted successfully!'}), 204
