import time
import datetime
import paho.mqtt.client as mqtt
import fourletterphat as flp
import buttonshim
import signal

## initialize variables
contract = "none"
display = "none"
bond = "+"
maxtemp = 30
checkout = False
print("Start: contract=",contract,", display=",display,", maxtemp=",maxtemp)
flp.clear
flp.print_str("INIT")
flp.show()

## Define event handlers

def on_connect(mqtt_client, obj, flags, rc):
    mqtt_client.subscribe("smartys1/temp")
    print("Connected")
    # loop_flag=0

def on_message(mqtt_client, obj, msg):
    message = msg.payload.decode()
    global temp
    temp = float(message) # + 100
    print("Topic: "+msg.topic+" Payload: "+message)
    print(datetime.datetime.now())

## set LED color based on temperature and max temperature
    global maxtemp
    if temp < (maxtemp - 2):
        print("green")
        buttonshim.set_pixel(0x00, 0xff, 0x00) #GREEN
    elif temp >= maxtemp:
        print("red")
        buttonshim.set_pixel(0xff, 0x00, 0x00) #RED
        global bond
        bond = "-"
    else:
        print("yellow")
        buttonshim.set_pixel(0xff, 0xff, 0x00) #YELLOW
## define display and set max temp measured
    global contract
    if contract == "none":
        flp.clear
        flp.print_str("STRT")
        flp.show()
        print("contract = none?",contract)
    elif contract == "bond":
        flp.clear
        flp.print_str("BOND")
        flp.show()
        print("contract = bond?",contract)
    elif contract == "started":
        ## set maximum measured temperature
        global maxtempmeasured
        print("contract = started?",contract)
        if float(maxtempmeasured) < temp:
            maxtempmeasured = message
            print("maxtempmeasured =",maxtempmeasured)
        ## define display
        global display
        print("display-def = ",display)
        if display == "max":
            print("Max Temp Measured = ", maxtempmeasured)
            flp.clear
            flp.print_str(maxtempmeasured)
            flp.show()
            if float(maxtempmeasured) < (maxtemp - 2):
                buttonshim.set_pixel(0x00, 0xff, 0x00) #GREEN
            elif float(maxtempmeasured) >= maxtemp:
                buttonshim.set_pixel(0xff, 0x00, 0x00) #RED
            else:
                buttonshim.set_pixel(0xff, 0xff, 0x00) #YELLOW
            display = "actual"
        else:
            print("display = Actual")
            flp.clear
            flp.print_str(message)
            flp.show()

## When a button is pushed, the temp and action is send to the smart contract

## define buttons:
buttonshim.NAMES = ['A-Start', 'B-Bond', 'C-Maxtemp', 'D-Accept', 'E-Reject']
print(buttonshim.NAMES)

## A = STRT (simulates escrow payment of transport fee by manufacturer)
@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    print("Button A")
    global contract
    if contract != "started":
        if contract != "bond":
            global display
            display = "bond"
            contract = "bond"
            print("A-if: contract = ",contract,", display = ", display)
        else:
            print("A-else: contract = ",contract,", display = ", display)
    else:
        print("A-contract = ",contract)  

## B = BORG (new function to simulate escrow payment of bond by transporter)
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    print("Button B")
    global contract
    if contract == "bond":
        print("B: In if-loop")
        ## capture and set initial temperatures
        firsttemp = temp
        global maxtempmeasured
        maxtempmeasured = temp
        global display
        display = "actual"
        global checkout
        checkout = False
        contract = "started"
        print("B-if: contract = ",contract,"firsttemp = ",firsttemp)
        ## send temp and start time to smart contract
        ## receive smart contract confirmation
        # return contract
    else:
        print("B-else = ",contract)  

## C = Show max temp
@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    print("Button c")
    global contract
    ## display max measured temp
    if contract == "started":
        global display
        display = "max"
        ## enable checkout via button D or E
        global checkout
        checkout = True
        print("C-if: contract = ",contract,", display = ", display,", checkout = ",checkout)
    else:
        print("C-else = ",contract)  

## D = Accept payment & Stop/Reset max temp
@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    print("Button D")
    global checkout
    if checkout == True:
        ## display Reject    
        global display
        display = "none"
        global contractmaxtemp
        contractmaxtemp = maxtempmeasured
        global contract
        contract = "stopped"
        flp.clear
        if bond == "-":
            flp.print_str("ACP-")
        else:
            flp.print_str("ACP+")
        flp.show()
        ## send reject message to smart contract
        ## receive smart contract confirmation    
        print("D-if: checkout = ",checkout,", contractmaxtemp = ", contractmaxtemp,", contract = ",contract)
    else:
        print("D-else: Geen checkout geweest")

## E = Reject payment & Stop/Reset max temp)
@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    print("Button E")
    global checkout
    if checkout == True:
        ## display Accept    
        global display
        display = "none"
        global contractmaxtemp
        contractmaxtemp = maxtempmeasured
        global contract
        contract = "stopped"
        flp.clear
        if bond == "-":
            flp.print_str("RJC-")
        else:
            flp.print_str("RJC+")
        flp.show()
        ## send reject message to smart contract
        ## receive smart contract confirmation   
        print("E-if: checkout = ",checkout,", contractmaxtemp = ", contractmaxtemp,", contract = ",contract)
    else:
        print("E-else: Geen checkout geweest")

print("Subscribing to EnviroPhat temperature via MQTT on broker.hivemq.com with topic smartys1/temp (CTRL-C to exit)")

mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)     # Create new instance
mqtt_client.on_connect = on_connect                         # Attach function to on_connect event
mqtt_client.on_message = on_message                         # Attach function to on_message event
mqtt_client.connect("broker.hivemq.com", 1883, 60)          # Connect to broker
mqtt_client.loop_start()                                    # Start loop to process callbacks

# loop_flag=1
# counter=0
# print("connect loop")
# while loop_flag==1:
#    print("waiting for callback ", counter)
#    time.sleep(1)                                        # Pauze 1/100 second
#    counter+=1
    
# signal.pause()

while True:
    mqtt_client = mqtt.Client("", True, None, mqtt.MQTTv31)     # Create new instance
    mqtt_client.loop_start()                                    # Start loop to process callbacks
    mqtt_client.on_connect = on_connect                         # Attach function to on_connect event
    mqtt_client.on_message = on_message                         # Attach function to on_message event
    mqtt_client.connect("broker.hivemq.com", 1883, 60)          # Connect to broker
    time.sleep(3)
    mqtt_client.disconnect
    mqtt_client.loop_stop()
    time.sleep(10)
