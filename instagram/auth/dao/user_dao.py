class UserDAO:
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        cursor = self.db.cursor()
        query = "SELECT username, email, created_at FROM User"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_user_stories(self, user_id):
        cursor = self.db.cursor()
        query = (f"""SELECT Story.story_id, Story.created_at, User.username,
                     User.email, Media.media_type, Media.media_url FROM Story
                     INNER JOIN User on User.user_id = Story.user_id
                     INNER JOIN Media on Media.media_id = Story.media_id
                     WHERE Story.user_id = {user_id}""")
        cursor.execute(query)
        stories = cursor.fetchall()
        cursor.close()
        return stories

    def get_hashtags_from_user_stories(self, user_id):
        cursor = self.db.cursor()
        query = f"""SELECT 
                        Story.story_id,
                        Story.created_at AS story_created_at,
                        Hashtag.tag AS hashtag
                    FROM 
                        Story
                    JOIN 
                        User on Story.user_id = User.user_id
                    JOIN 
                        StoryHashtag ON Story.story_id = StoryHashtag.story_id
                    JOIN 
                        Hashtag ON StoryHashtag.hashtag_id = Hashtag.hashtag_id
                    WHERE 
                        User.user_id = {user_id}
                    ORDER BY 
                       Story.story_id, Hashtag.tag;
                 """
        cursor.execute(query)
        hashtags = cursor.fetchall()
        cursor.close()
        return hashtags

    def insert_user(self, username, email, password):
        try:
            cursor = self.db.cursor()
            query = (f"INSERT INTO User (username, email, password) VALUES ("
                     f"{username}, {email}, {password})")
            cursor.execute(query)
            self.db.commit()
            cursor.close()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_user(self, user_id, username=None, email=None, password=None):
        try:
            cursor = self.db.cursor()
            query = "UPDATE User SET "
            fields = []
            values = []

            if username:
                fields.append("username = %s")
                values.append(username)

            if email:
                fields.append("email = %s")
                values.append(email)

            if password:
                fields.append("password = %s")
                values.append(password)

            if fields:
                query += ", ".join(fields) + " WHERE user_id = %s"
                values.append(user_id)
                cursor.execute(query, tuple(values))
                self.db.commit()
            cursor.close()
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_story(self, user_id, story_id):
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT user_id FROM Story WHERE story_id = {user_id}")
            result = cursor.fetchone()

            if result is None:
                return {'message': 'Story not found.'}, 404

            story_user_id = result[0]

            if story_user_id != user_id:
                return {'message': 'You are not authorized to delete this story.'}, 403

            cursor.execute(f"DELETE FROM Feed WHERE story_id = {story_id}")
            cursor.execute(f"DELETE FROM Reaction WHERE story_id = {story_id}")

            query = f"DELETE FROM Story WHERE story_id = {story_id}"
            cursor.execute(query)
            self.db.commit()
            cursor.close()

            return {'message': 'Story deleted successfully!'}, 204

        except Exception as e:
            self.db.rollback()
            raise e
