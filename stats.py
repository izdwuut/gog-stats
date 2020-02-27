import os
from configparser import ConfigParser
from reddit import Reddit

class Stats:
    def get_submission_type_breakdown(self):
        types = {'gog': 0, 'offer': 0, 'intro': 0, 'request': 0, 'discussion': 0, 'announcement': 0}
        for submission in self.reddit.get_subreddit(self.config['reddit']['subreddit']).new(limit=1000):
            for type in types.keys():
                if type in self.reddit.get_submission_title(submission).lower():
                    types[type] += 1
            print('Processed thread {}.'.format(self.reddit.get_submission_title(submission)))
        return self.get_csv(types)

    def get_offers_count(self):
        users = {}
        for submission in self.reddit.get_subreddit(self.config['reddit']['subreddit']).new(limit=1000):
            if not self.reddit.get_author(submission) or 'offer' not in self.reddit.get_submission_title(submission).lower():
                continue
            author = self.reddit.get_author(submission).name
            if author not in users:
                users[author] = 0
            users[author] += 1
            print('Processed thread {}.'.format(self.reddit.get_submission_title(submission)))

        count_aggregated = {}
        for user, count in users.items():
            if count not in count_aggregated:
                count_aggregated[count] = 0
            count_aggregated[count] += 1
        return self.get_csv(count_aggregated)

    def get_how_often_users_request_games(self):
        users = {}
        for submission in self.reddit.get_subreddit(self.config['reddit']['subreddit']).new(limit=1000):
            if not self.reddit.get_author(submission) or 'request' not in self.reddit.get_submission_title(submission).lower():
                continue
            author = self.reddit.get_author(submission).name
            if author not in users:
                users[author] = 0
            users[author] += 1
            print('Processed thread {}.'.format(self.reddit.get_submission_title(submission)))

        count_aggregated = {}
        for user, count in users.items():
            if count not in count_aggregated:
                count_aggregated[count] = 0
            count_aggregated[count] += 1
        return self.get_csv(count_aggregated)

    def get_how_often_users_participate_in_giveaways(self):
        users = {}
        for submission in self.reddit.get_subreddit(self.config['reddit']['subreddit']).new(limit=1000):
            if not self.reddit.get_author(submission) or 'offer' not in self.reddit.get_submission_title(
                    submission).lower():
                continue
            for comment in submission.comments:
                if not self.reddit.get_author(comment):
                    continue
                author = self.reddit.get_author(comment).name
                if author not in users:
                    users[author] = 0
                users[author] += 1
            print('Processed thread {}.'.format(self.reddit.get_submission_title(submission)))

        count_aggregated = {}
        for user, count in users.items():
            if count not in count_aggregated:
                count_aggregated[count] = 0
            count_aggregated[count] += 1
        return self.get_csv(count_aggregated)

    def get_how_much_users_give_back_to_community(self):
        users = {}
        for submission in self.reddit.get_subreddit(self.config['reddit']['subreddit']).new(limit=1000):
            if not self.reddit.get_author(submission) or 'offer' not in self.reddit.get_submission_title(
                    submission).lower():
                continue
            submission_author = self.reddit.get_author(submission).name
            if submission_author not in users:
                users[submission_author] = {'offered': 0, 'participated': 0}
            users[submission_author]['offered'] += 1
            for comment in submission.comments:
                if not self.reddit.get_author(comment):
                    continue
                comment_author = self.reddit.get_author(comment).name
                if comment_author not in users:
                    users[comment_author] = {'offered': 0, 'participated': 0}
                users[comment_author]['participated'] += 1
            print('Processed thread {}.'.format(self.reddit.get_submission_title(submission)))

        aggregated = ['offered,participated']
        for stats in users.values():
            aggregated.append('{},{}'.format(stats['offered'], stats['participated']))
        return '\n'.join(aggregated)

    def get_csv(self, items):
        for key, value in items.items():
            print('{},{}'.format(key, value))

    def __init__(self, settings='settings.ini'):
        self.config = ConfigParser(os.environ)
        self.config.read(settings)
        self.reddit = Reddit(self.config['reddit'])


if __name__ == '__main__':
    stats = Stats()
    print(stats.get_how_much_users_give_back_to_community())
