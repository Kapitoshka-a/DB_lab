class CommentDAO:
    def __init__(self, db):
        self.db = db

    def insert_comment(self, story_id, user_id, content):
        cursor = self.db.cursor()
        query = "CALL insert_comment(%s, %s, %s)"
        cursor.execute(query, (story_id, user_id, content))
        cursor.close()

    def insert_new_story_hashtag_connection(self, story_id, tag):
        cursor = self.db.cursor()
        query = "CALL insert_new_story_hashtag_connection(%s, %s)"
        cursor.execute(query, (story_id, tag))
        cursor.close()

    def insert_multiple_comments(self, story_id, user_id):
        cursor = self.db.cursor()
        query = "CALL insert_multiple_comments(%s, %s)"
        cursor.execute(query, (story_id, user_id))
        cursor.close()

    def get_avg_comment_length(self):
        cursor = self.db.cursor()
        query = "CALL get_avg_comment_length_proc()"
        cursor.execute(query)
        avg_length = cursor.fetchone()
        cursor.close()
        return avg_length

    def create_random_comment_tables(self):
        cursor = self.db.cursor()
        query = "CALL create_random_comment_tables()"
        cursor.execute(query)
        cursor.close()
