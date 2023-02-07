from google.cloud import pubsub_v1
import json

with open('config2.json') as config_file:
    config = json.load(config_file)

project_id = config['project_id']
topic_name = config['topic_name']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id,topic_name)

message = "Hi, I'm publishing some data"
message_data = message.encode("utf-8")

publisher.publish(topic_path,data=message_data)
print("Message published.")



