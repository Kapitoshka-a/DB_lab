class UserDTO:
    def __init__(self, username, email, created_at):
        self.username = username
        self.email = email
        self.created_at = created_at

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }


class UserStoryDTO:
    def __init__(self, story_id, created_at, username, email, media_type, media_url):
        self.story_id = story_id
        self.created_at = created_at
        self.username = username
        self.email = email
        self.media_type = media_type
        self.media_url = media_url

    def to_dict(self):
        return {
            'story_id': self.story_id,
            'created_at': self.created_at,
            'username': self.username,
            'email': self.email,
            'media_type': self.media_type,
            'media_url': self.media_url
        }


class HashtagDTO:
    def __init__(self, story_id, story_created_at, hashtag):
        self.story_id = story_id
        self.story_created_at = story_created_at
        self.hashtag = hashtag

    def to_dict(self):
        return {
            'story_id': self.story_id,
            'story_created_at': self.story_created_at,
            'hashtag': self.hashtag
        }