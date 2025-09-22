from instagram.base.connector import get_connection


class UserDAO:
    @staticmethod
    def get_all_users():
        query = "SELECT user_id, username, email, created_at FROM User"
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def get_users_id():
        query = "SELECT user_id FROM User"
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def get_user_stories(self, user_id):
        query = """
            SELECT Story.story_id, Story.created_at, User.username,
                   User.email, Media.media_type, Media.media_url
            FROM Story
            INNER JOIN User ON User.user_id = Story.user_id
            INNER JOIN Media ON Media.media_id = Story.media_id
            WHERE Story.user_id = %s
        """
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

    @staticmethod
    def get_hashtags_from_user_stories(self):
        query = """
            SELECT 
                User.username,
                Story.story_id,
                Story.created_at AS story_created_at,
                Hashtag.tag AS hashtag
            FROM Story
            JOIN User ON Story.user_id = User.user_id
            JOIN StoryHashtag ON Story.story_id = StoryHashtag.story_id
            JOIN Hashtag ON StoryHashtag.hashtag_id = Hashtag.hashtag_id
            ORDER BY Story.story_id, Hashtag.tag
        """
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def insert_user(self, username, email, password):
        query = "INSERT INTO User (username, email, password) VALUES (%s, %s, %s)"
        with get_connection() as conn, conn.cursor() as cursor:
            try:
                cursor.execute(query, (username, email, password))
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    @staticmethod
    def update_user(self, user_id, username=None, email=None, password=None):
        fields, values = [], []

        if username:
            fields.append("username = %s")
            values.append(username)
        if email:
            fields.append("email = %s")
            values.append(email)
        if password:
            fields.append("password = %s")
            values.append(password)

        if not fields:
            return  # nothing to update

        query = f"UPDATE User SET {', '.join(fields)} WHERE user_id = %s"
        values.append(user_id)

        with get_connection() as conn, conn.cursor() as cursor:
            try:
                cursor.execute(query, tuple(values))
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    @staticmethod
    def delete_story(self, user_id, story_id):
        try:
            with get_connection() as conn, conn.cursor() as cursor:
                cursor.execute("SELECT user_id FROM Story WHERE story_id = %s", (story_id,))
                result = cursor.fetchone()

                if result is None:
                    return {'message': 'Story not found.'}, 404

                story_user_id = result["user_id"]

                if story_user_id != user_id:
                    return {'message': 'You are not authorized to delete this story.'}, 403

                cursor.execute("DELETE FROM Feed WHERE story_id = %s", (story_id,))
                cursor.execute("DELETE FROM Reaction WHERE story_id = %s", (story_id,))
                cursor.execute("DELETE FROM Story WHERE story_id = %s", (story_id,))
                conn.commit()

                return {'message': 'Story deleted successfully!'}, 204

        except Exception:
            conn.rollback()
            raise
