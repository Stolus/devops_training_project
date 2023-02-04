from flask import Flask, jsonify
import google.cloud
from google.cloud.pubsub_v1 import PublisherClient

app = Flask(__name__)

project_id = ""
topic_name = ""
publisher: PublisherClient = google.cloud.pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id,topic_name)

@app.route("/")
def index():
    return "Welcome to the DevOps project API service"

@app.route("/publish/<message>", methods=["POST"])
def publish(message):
    message_data = message.encode("utf-8")
    publisher.publish(topic_path, data=message_data)
    return jsonify({"message": "Published successfully"}), 201

@app.route("/messages", method=["GET"])
def message():
    subscriber = google.cloud.pubsub_v1.SubscriberClient()
    subscription_name = "this-subscription-name"
    subscription_path = subscriber.subscription_path(project_id,subscription_name)
    messages = []
    try:
        response = subscriber.pull(subscription_path, max_messages=10)
        messages = [message.data.decode("utf-8") for message in response.received_messages]
        ack_ids = [message.ack_ids for message in response.received_messages]
        subscriber.acknowledge(subscription_path, ack_ids)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    return jsonify({"messages": messages}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)





