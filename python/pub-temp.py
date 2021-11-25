import time
import datetime

from envirophat import weather

import paho.mqtt.client as mqtt

def on_connect(mqtt_client, obj, flags, rc):
    print("Connected")

# Define on_publish event Handler
def on_publish(client, userdata, mid):
    print("Message Published...")

mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

print("Publishing temperature via MQTT to broker.hivemq.com with topic smartie1/temp (CTRL-C to exit)")

#mqtt_client.loop_forever()
try:
    while True:
        timestamp = datetime.datetime.now().isoformat()
        temp = round(weather.temperature(),1) -9
        message = temp,"| ",timestamp
        mqtt_client.connect("broker.hivemq.com",1883)
        mqtt_client.publish("smartie1/temp",temp)
        print(temp,"| ",timestamp)
        mqtt_client.disconnect()
        time.sleep(10)

# exit the script with ctrl-c
except KeyboardInterrupt:
    print("Session interrupted")


