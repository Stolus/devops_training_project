from google.cloud import pubsub_v1
import json

with open('config3.json') as config_file:
    config = json.load(config_file)

project_id = config['project_id']
subscription_name = config['this-subscription-name']

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print("Received message: {}".format(message.data))
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for message on {}..\n".format(subscription_path))
