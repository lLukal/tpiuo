import json
import praw
from praw.models import Submission
from azure.eventhub import EventHubProducerClient, EventData


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
top_posts = subreddit.top(limit=reddit_post_limit, time_filter='all')



# Azure Event Hub part
producer_client = EventHubProducerClient.from_connection_string(conn_str=eventhub_connection_str, eventhub_name=eventhub_name)

with producer_client:
    for post in top_posts:
        print('------------------------')
        print('Sending post to Event Hub...')
        
        json_data = json.dumps(post, default=submission_serializer)

        event_data = EventData(body=json_data)
        producer_client.send_event(event_data)
        
        print('\tDone!')
        print('------------------------')

    while True:
        continue
