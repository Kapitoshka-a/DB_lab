from flask import Blueprint, request, jsonify

from instagram.base.config import config
from instagram.service.procedure_service import CommentService
from instagram.dao.procedure_dao import CommentDAO
import pymysql

comment_bp = Blueprint('comment', __name__)


db = pymysql.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
    port=config.DB_PORT
)
comment_dao = CommentDAO(db)
comment_service = CommentService(comment_dao)


@comment_bp.route('/comments', methods=['POST'])
def insert_comment():
    """
    Insert a new comment for a story
    ---
    tags:
      - Comments
    summary: Create a new comment
    description: Creates a new comment for a specific story by a user
    parameters:
      - name: body
        in: body
        required: true
        description: Comment data
        schema:
          type: object
          required:
            - story_id
            - user_id
            - content
          properties:
            story_id:
              type: integer
              description: ID of the story being commented on
              example: 1
            user_id:
              type: integer
              description: ID of the user creating the comment
              example: 123
            content:
              type: string
              description: The comment text content
              example: "Great story! Really enjoyed reading it."
              minLength: 1
              maxLength: 500
    responses:
      201:
        description: Comment created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Comment inserted successfully!"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required fields"
      404:
        description: Story or user not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Story not found"
    """
    data = request.get_json()
    story_id = data['story_id']
    user_id = data['user_id']
    content = data['content']
    comment_service.insert_comment(story_id, user_id, content)
    return jsonify({'message': 'Comment inserted successfully!'}), 201


@comment_bp.route('/story/hashtag', methods=['POST'])
def insert_new_story_hashtag_connection():
    """
    Create a connection between a story and a hashtag
    ---
    tags:
      - Stories
      - Hashtags
    summary: Link story with hashtag
    description: Creates a relationship between a story and a hashtag for categorization and discovery
    parameters:
      - name: body
        in: body
        required: true
        description: Story-hashtag connection data
        schema:
          type: object
          required:
            - story_id
            - tag
          properties:
            story_id:
              type: integer
              description: ID of the story to tag
              example: 1
            tag:
              type: string
              description: Hashtag text (without # symbol)
              example: "travel"
              pattern: "^[a-zA-Z0-9_]+$"
              minLength: 1
              maxLength: 50
    responses:
      201:
        description: Story hashtag connection created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Story hashtag connection created!"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid hashtag format"
      404:
        description: Story not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Story not found"
    """
    data = request.get_json()
    story_id = data['story_id']
    tag = data['tag']
    comment_service.insert_new_story_hashtag_connection(story_id, tag)
    return jsonify({'message': 'Story hashtag connection created!'}), 201


@comment_bp.route('/comments/multiple', methods=['POST'])
def insert_multiple_comments():
    """
    Insert multiple comments for a story by a user
    ---
    tags:
      - Comments
    summary: Bulk insert comments
    description: Creates multiple comments for a specific story by a user (useful for testing or bulk operations)
    parameters:
      - name: body
        in: body
        required: true
        description: Data for multiple comment insertion
        schema:
          type: object
          required:
            - story_id
            - user_id
          properties:
            story_id:
              type: integer
              description: ID of the story to comment on
              example: 1
            user_id:
              type: integer
              description: ID of the user creating comments
              example: 123
    responses:
      201:
        description: Multiple comments inserted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Multiple comments inserted!"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required fields"
      404:
        description: Story or user not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Story or user not found"
    """
    data = request.get_json()
    story_id = data['story_id']
    user_id = data['user_id']
    comment_service.insert_multiple_comments(story_id, user_id)
    return jsonify({'message': 'Multiple comments inserted!'}), 201


@comment_bp.route('/comments/avg_length', methods=['GET'])
def get_avg_comment_length():
    """
    Get the average length of all comments
    ---
    tags:
      - Comments
      - Analytics
    summary: Calculate average comment length
    description: Returns the average character length of all comments in the system for analytics purposes
    responses:
      200:
        description: Average comment length calculated successfully
        schema:
          type: object
          properties:
            avg_comment_length:
              type: number
              format: float
              description: Average length of comments in characters
              example: 45.7
        examples:
          application/json:
            avg_comment_length: 45.7
      500:
        description: Database error occurred
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unable to calculate average length"
    """
    avg_length = comment_service.get_avg_comment_length()
    return jsonify({'avg_comment_length': avg_length[0]}), 200


@comment_bp.route('/comments/random_tables', methods=['POST'])
def create_random_comment_tables():
    """
    Create random comment tables for testing
    ---
    tags:
      - Comments
      - Testing
      - Database
    summary: Generate test data tables
    description: Creates random comment tables with test data for development and testing purposes
    responses:
      201:
        description: Random comment tables created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Random comment tables created!"
      500:
        description: Database error occurred during table creation
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Failed to create random tables"
    """
    comment_service.create_random_comment_tables()
    return jsonify({'message': 'Random comment tables created!'}), 201