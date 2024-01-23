import json
import time
import praw
from praw.models import Submission
from azure.eventhub import EventHubProducerClient, EventData
import logging


creds = {}
# Load credentials from creds.json
with open('creds.json') as f:
    creds = json.load(f)
    #print(creds)


reddit_client_id = creds['reddit_client_id']
reddit_client_secret = creds['reddit_client_secret']
reddit_user_agent = creds['reddit_user_agent']
reddit_username = creds['reddit_username']
reddit_password = creds['reddit_password']
reddit_subreddit = "dataengineering"
reddit_post_limit = 10
eventhub_connection_str = creds['eventhub_connection_str']
eventhub_name = creds['eventhub_name']


# Helper function for serializing Submission object to JSON
def submission_serializer(submission):
    if isinstance(submission, Submission):
        return {
            key: getattr(submission, key) for key in dir(submission) if not key.startswith('_')
        }


# Reddit API part
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent,
                     username=reddit_username,
                     password=reddit_password)
subreddit = reddit.subreddit(reddit_subreddit)


# Azure Event Hub part
producer_client = EventHubProducerClient.from_connection_string(conn_str=eventhub_connection_str, eventhub_name=eventhub_name)

with producer_client:
    after_param = ''
    for _ in range(100):
        logging.warning('------------------------')
        logging.warning(f'Sending next {reddit_post_limit} posts to Event Hub...')
        
        all_posts = []
        top_posts = subreddit.top(limit=reddit_post_limit, time_filter='all', params={'after': after_param})
        json_data = None
        
        for post in top_posts:
            json_data = json.dumps(post, default=submission_serializer)
            event_data = EventData(body=json_data)
            all_posts.append(event_data)

        # batch_event_data = EventData(body=json.dumps(all_posts))
        producer_client.send_batch(all_posts)
        after_param = json.loads(json_data)['fullname'] if top_posts else ''
        
        logging.warning(f'\tDone...')
        logging.warning('------------------------')
        
        time.sleep(10)

    while True:
        continue
