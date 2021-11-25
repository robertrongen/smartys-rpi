import time
import datetime
import paho.mqtt.client as mqtt
import fourletterphat as flp
import signal
import buttonshim

# set max temperature
maxtemp = 30

# Define event handlers

def on_connect(mqtt_client, obj, flags, rc):
    mqtt_client.subscribe("smartys1/temp")
    print("Connected")

def on_message(mqtt_client, obj, msg):
    message = msg.payload.decode()
    temp = float(message) # + 100
    print("Topic: "+msg.topic+" Payload: "+message)
    print(datetime.datetime.now())
    flp.print_str(message)
    flp.show()
# set LED color based on temperature and max temperature
    if temp < (maxtemp - 2):
        print("green")
        buttonshim.set_pixel(0x00, 0xff, 0x00) #GREEN
    elif temp > maxtemp:
        print("red")
        buttonshim.set_pixel(0xff, 0x00, 0x00) #RED
    else:
        print("yellow")
        buttonshim.set_pixel(0xff, 0xff, 0x00) #YELLOW

print("Subscribing to EnviroPhat temperature via MQTT on broker.hivemq.com with topic smartie1/temp (CTRL-C to exit)")

mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("broker.hivemq.com", 1883, 60)

mqtt_client.loop_forever()
