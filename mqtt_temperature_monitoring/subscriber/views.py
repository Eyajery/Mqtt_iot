# mqtt_subscriber/views.py
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import paho.mqtt.client as mqtt
import threading
import random
import time
from .models import Temperature

class TemperatureSubscriber(View):
    temperature_lock = threading.Lock()
    connected_event = threading.Event()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            print("Connexion réussie.")
            self.connected_event.set()
            client.subscribe("temp", qos=1)
        else:
            print("Échec de la connexion avec le code %s." % rc)

    def on_message(self, client, userdata, msg):
        received_temperature = float(msg.payload.decode())
        print("Température reçue:", received_temperature)

        with self.temperature_lock:
            Temperature.objects.create(value=received_temperature)

    def generate_and_publish_temperature(self, client):
        while True:
            random_temperature = round(random.uniform(18.0, 25.0), 2)
            print("Température générée aléatoirement:", random_temperature)

            client.publish("temp", payload=str(random_temperature), qos=1)
            time.sleep(10)

    def get(self, request):
        client = mqtt.Client(client_id="django_subscriber", protocol=mqtt.MQTTv5)
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set("eya.jery", "aya06122000.A")
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("9e8337d83d4c453986761fe694d9a4f4.s2.eu.hivemq.cloud", 8883)
        client.loop_start()

        temperature_thread = threading.Thread(target=self.generate_and_publish_temperature, args=(client,))
        temperature_thread.start()

        self.connected_event.wait()

        with self.temperature_lock:
            last_temperature = Temperature.objects.order_by('-timestamp').first()

            # Récupérer toutes les données de température
            temperatures = Temperature.objects.all().order_by('timestamp')
            temperature_data = [{'timestamp': temp.timestamp.isoformat(), 'value': temp.value} for temp in temperatures]

            return render(request, 'temperature.html', {'last_temperature': last_temperature, 'temperature_data': temperature_data})