import os
from pathlib import Path

import pandas as pd
import yaml
import praw
from praw.models import MoreComments

SECRETS_PATH = os.path.join(Path(__file__).parents[3], 'secrets')

# Source: https://praw.readthedocs.io/en/latest/tutorials/comments.html
class Reddit:
    def __init__(self):
        client_id, secret_id = self._get_reddit_secrets()
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction (by u/TampaTurtle)",
            client_id=client_id,
            client_secret=secret_id,
            )

    def _get_reddit_secrets(self):
        path = os.path.join(SECRETS_PATH, 'reddit.yaml')
        with open(path, 'r') as file:
            secrets = yaml.safe_load(file)
        return secrets.get('client_id'), secrets.get('secret_id')

    def get_top_level_comments(self, id):
        submission = self.reddit.submission(id=id)
        return {
            ix: {
                'body':comment.body,
                'upvotes':comment.score,
                'id': comment.id,
                'parent_id': None,
                'subreddit_id': comment.subreddit_id,
                }
            for ix, comment in enumerate(submission.comments)
            }

    def get_all_comments(self, id):
        submission = self.reddit.submission(id=id)
        submission.comments.replace_more(limit=None)
        return {
            ix: {
                'body':comment.body,
                'upvotes':comment.score,
                'id': comment.id,
                'parent_id': comment.parent_id,
                'subreddit_id': comment.subreddit_id
                }
            for ix, comment in enumerate(submission.comments.list())
            }

    def get_all_comments_formatted(self, id):
        submission = self.reddit.submission(id=id)
        submission.comments.replace_more(limit=None)
        comments = [
            [
                comment.id,
                comment.body,
                comment.score,
                comment.parent_id,
                comment.subreddit_id
                ]
            for ix, comment in enumerate(submission.comments.list())
            ]
        cols = [
            'id',
            'text',
            'upvotes',
            'parent_id',
            'subreddit_id'
        ]
        comments = pd.DataFrame(comments, columns=cols)
        return comments
