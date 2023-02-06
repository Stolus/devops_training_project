# Pycharm mi podkreśla formatowanie generalne, typu brak spacji po przecinkach, za mało odstępów,
# warto sobie klikać w IDE "formatuj plik" bo wtedy jest ładniej i czytelniej

from flask import Flask, jsonify
import google.cloud
from google.cloud.pubsub_v1 import PublisherClient

app = Flask(__name__)

# to project_id, topic_name bym sobie wyciągnął do pliku konfiguracyjnego
# albo używał chociaż zmiennej środowiskowej
# bo to jest typowa konfiguracja aplikacji
# np. jakbyśmy mieli środowisko dev, test, prod to wtedy byśmy chcieli mieć różne wartości
# dla tych zmiennych, więc nie przeszłoby zahardcodowanie tego

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

# Trochę nie rozumiem do końca tego endpointa
# Bo on tutaj jakby pulluje wiadomości z subscribera (czyli już jakby to są te wiadomości które dostały message.ack z callbacku subscribera, tak?)
# I potem robi subscriber.acknowledge na tych wiadomościach, czyli czy to coś zmienia?
# Bo te wiadomości już chyba były wcześniej zacknowledgeowane przez subscribera?
# Czy własnie czegoś nie rozumiem.
@app.route("/messages", method=["GET"])
def message():
    subscriber = google.cloud.pubsub_v1.SubscriberClient()

    # tak samo, to bym dodał do configa
    subscription_name = "this-subscription-name"
    subscription_path = subscriber.subscription_path(project_id,subscription_name)
    messages = [] # nieużuywana zmienna, bo poniżej tworzona jest od zera
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






