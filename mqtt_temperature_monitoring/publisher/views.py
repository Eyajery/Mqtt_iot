from django.http import HttpResponse
from django.views import View
import paho.mqtt.client as mqtt
import random

class TemperaturePublisher(View):
    def get(self, request):
        # Création d'un client MQTT pour le Publisher (Agent-capteur)
        client = mqtt.Client(client_id="django_publisher", protocol=mqtt.MQTTv5)
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

        # Configuration du nom d'utilisateur et du mot de passe pour le broker MQTT
        client.username_pw_set("eya.jery", "aya06122000.A")
        client.connect("9e8337d83d4c453986761fe694d9a4f4.s2.eu.hivemq.cloud", 8883)

        # Génération d'une valeur aléatoire de température
        random_temperature = round(random.uniform(18.0, 25.0), 2)

        # Publication de la température sur le topic "Temp"
        client.publish("Temp", payload=str(random_temperature), qos=1)

        # Déconnexion du broker MQTT
        client.disconnect()

        return HttpResponse(f"Temperature published: {random_temperature} °C")

