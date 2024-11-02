from instagram.auth.dao.user_dao import UserDAO

class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_all_users(self):
        return self.user_dao.get_all_users()

    def get_users_ids(self):
        return self.user_dao.get_users_id()

    def create_user(self, username, email, password):
        return self.user_dao.insert_user(username, email, password)

    def get_user_stories(self, user_id):
        return self.user_dao.get_user_stories(user_id)

    def get_hashtags_from_user_stories(self):
        return self.user_dao.get_hashtags_from_user_stories()

    def update_user(self, user_id, username, email, password):
        return self.user_dao.update_user(user_id, username, email, password)

    def delete_story(self, user_id, story_id):
        return self.user_dao.delete_story(user_id, story_id)