import praw

class Reddit:
    def get_subreddit(self, subreddit):
        return self.api.subreddit(subreddit)

    def get_submission_title(self, submission):
        return submission.title

    def get_author(self, item):
        return item.author

    def __init__(self, config):
        self.api = praw.Reddit(client_id=config['client_id'],
                               client_secret=config['client_secret'],
                               user_agent=config['user_agent'])

