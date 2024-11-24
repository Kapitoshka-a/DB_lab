# routes.py
from flask import Blueprint, request, jsonify
from config.config import Config
from instagram.auth.service.procedure_service import CommentService
from instagram.auth.dao.procedure_dao import CommentDAO
import pymysql

comment_bp = Blueprint('comment', __name__)

# Database configuration
config = Config()
db = pymysql.connect(host=config.DB_HOST,
                     user=config.DB_USER,
                     password=config.DB_PASSWORD,
                     database=config.DB_NAME)

# Initialize DAO and Service
comment_dao = CommentDAO(db)
comment_service = CommentService(comment_dao)


# Insert comment
@comment_bp.route('/comments', methods=['POST'])
def insert_comment():
    data = request.get_json()
    story_id = data['story_id']
    user_id = data['user_id']
    content = data['content']

    comment_service.insert_comment(story_id, user_id, content)
    return jsonify({'message': 'Comment inserted successfully!'}), 201


# Insert new story hashtag connection
@comment_bp.route('/story/hashtag', methods=['POST'])
def insert_new_story_hashtag_connection():
    data = request.get_json()
    story_id = data['story_id']
    tag = data['tag']

    comment_service.insert_new_story_hashtag_connection(story_id, tag)
    return jsonify({'message': 'Story hashtag connection created!'}), 201


# Insert multiple comments
@comment_bp.route('/comments/multiple', methods=['POST'])
def insert_multiple_comments():
    data = request.get_json()
    story_id = data['story_id']
    user_id = data['user_id']

    comment_service.insert_multiple_comments(story_id, user_id)
    return jsonify({'message': 'Multiple comments inserted!'}), 201


# Get average comment length
@comment_bp.route('/comments/avg_length', methods=['GET'])
def get_avg_comment_length():
    avg_length = comment_service.get_avg_comment_length()
    return jsonify({'avg_comment_length': avg_length[0]}), 200


# Create random comment tables
@comment_bp.route('/comments/random_tables', methods=['POST'])
def create_random_comment_tables():
    comment_service.create_random_comment_tables()
    return jsonify({'message': 'Random comment tables created!'}), 201
