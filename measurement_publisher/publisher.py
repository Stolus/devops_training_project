from google.cloud import pubsub_v1

project_id = "project-id"
topic_name = "topic-name"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id,topic_name)

message = "Hi, I'm publishing some data"
message_data = message.encode("utf-8")

publisher.publish(topic_path,data=message_data)
print("Message published.")



