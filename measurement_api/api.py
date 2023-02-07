# warto sobie klikać w IDE "formatuj plik" bo wtedy jest ładniej i czytelniej
import json
from flask import Flask, jsonify
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient

app = Flask(__name__)

with open('config1.json') as config_file:
    config = json.load(config_file)

project_id = config['project_id']
topic_name = config['topic_name']

publisher = PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


@app.route("/")
def index():
    return "Welcome to the DevOps project API service"


@app.route("/publish/<message>", methods=["POST"])
def publish(message):
    message_data = message.encode("utf-8")
    publisher.publish(topic_path, data=message_data)
    return jsonify({"message": "Published successfully"}), 201

# Trochę nie rozumiem do końca tego endpointa
# Bo on tutaj jakby pulluje wiadomości z subscribera (czyli już jakby to są te wiadomości które dostały message.ack z callbacku subscribera, tak?)
# I potem robi subscriber.acknowledge na tych wiadomościach, czyli czy to coś zmienia?
# Bo te wiadomości już chyba były wcześniej zacknowledgeowane przez subscribera?
# Czy własnie czegoś nie rozumiem.


"""
Nie nie, endpoint /publish/<message> nie jest odpowiedzialny za pullowanie wiadomości z subscribera, 
tylko za publikowanie wiadomości do topicu. Pozwala wysłaać wiadomości do topicu, 
wykorzystując publisher.publish(topic_path, data=message_data). 
Po wysłaniu wiadomości, odpowiednie informacje zwrotne są zwracane do klienta. 
Ten endpoint jest udostępniany jako POST, więc wiadomość jest publikowana tylko wtedy, 
gdy wysyłamy zapytanie POST do tego endpointa.
"""


@app.route("/messages", method=["GET"])
def message():
    subscriber = SubscriberClient()

    subscription_name = config["subscription_name"]
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

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




