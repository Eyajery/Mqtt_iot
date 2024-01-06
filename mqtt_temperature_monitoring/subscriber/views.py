from django.http import JsonResponse
from django.views import View
import paho.mqtt.client as mqtt
import threading
import random
import time

class TemperatureSubscriber(View):
    temperature = None
    temperature_lock = threading.Lock()  # Verrou pour assurer la sécurité des threads
    connected_event = threading.Event()  # Événement pour signaler la connexion établie

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            print("Connexion réussie.")
            self.connected_event.set()  # Signal que la connexion est établie
            # Souscription au topic "Temp" lors de la connexion réussie
            client.subscribe("temp", qos=1)
        else:
            print("Échec de la connexion avec le code %s." % rc)

    def on_message(self, client, userdata, msg):
        # Analyse de la charge utile reçue en tant que flottant
        received_temperature = float(msg.payload.decode())
        print("Température reçue:", received_temperature)

        # Acquisition du verrou avant de mettre à jour la variable partagée
        with self.temperature_lock:
            self.temperature = received_temperature

    def generate_and_publish_temperature(self, client):
        while True:
            # Génération d'une valeur aléatoire de température
            random_temperature = round(random.uniform(18.0, 25.0), 2)
            print("Température générée aléatoirement:", random_temperature)

            # Publication de la température sur le topic "Temp"
            client.publish("temp", payload=str(random_temperature), qos=1)
            time.sleep(10)  # Ajustez l'intervalle de sommeil selon vos besoins

    def get(self, request):
        # Création d'un client MQTT pour le Subscriber (Agent-utilisateur)
        client = mqtt.Client(client_id="django_subscriber", protocol=mqtt.MQTTv5)
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

        # Configuration du nom d'utilisateur et du mot de passe pour le broker MQTT
        client.username_pw_set("eya.jery", "aya06122000.A")
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("9e8337d83d4c453986761fe694d9a4f4.s2.eu.hivemq.cloud", 8883)

        # Démarrage de la boucle du client MQTT
        client.loop_start()

        # Démarrage d'un thread séparé pour générer et publier périodiquement des valeurs de température
        temperature_thread = threading.Thread(target=self.generate_and_publish_temperature, args=(client,))
        temperature_thread.start()

        # Attente de l'établissement de la connexion
        self.connected_event.wait()

        # Acquisition du verrou avant d'accéder à la variable partagée
        with self.temperature_lock:
            # Retour de la dernière température générée en tant que réponse JSON
            return JsonResponse({"temperature": self.temperature})

