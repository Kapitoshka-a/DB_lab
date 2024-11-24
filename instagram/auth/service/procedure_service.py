

class CommentService:
    def __init__(self, comment_dao):
        self.comment_dao = comment_dao

    def insert_comment(self, story_id, user_id, content):
        self.comment_dao.insert_comment(story_id, user_id, content)

    def insert_new_story_hashtag_connection(self, story_id, tag):
        self.comment_dao.insert_new_story_hashtag_connection(story_id, tag)

    def insert_multiple_comments(self, story_id, user_id):
        self.comment_dao.insert_multiple_comments(story_id, user_id)

    def get_avg_comment_length(self):
        return self.comment_dao.get_avg_comment_length()

    def create_random_comment_tables(self):
        self.comment_dao.create_random_comment_tables()
