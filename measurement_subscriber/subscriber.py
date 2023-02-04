from google.cloud import pubsub_v1

project_id = "this-project-id"
subscription_name = "this-subscription-name"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print("Receved message: {}".format(message.data))
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for message on {}..\n".format(subscription_path))
