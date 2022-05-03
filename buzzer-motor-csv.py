#Import MQTT, time, GPIO, time and CSV writer
import paho.mqtt.client as mqttClient
import time
import RPi.GPIO as GPIO
from datetime import datetime
import csv

#SET UP GPIO PINS FOR STEPPER MOTOR AND BUZZER
#This uses GPIO.BOARD numbering i.e. the number on the board:
#1   2
#3   4
#5   6
...
#25  26
GPIO.setmode(GPIO.BOARD)

#Turn off GPIO warnings
GPIO.setwarnings(False)

#STEPPER MOTOR CODE
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ControlPin = [7,11,13,15]

for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, 0)   #False
    
#Stepper motor sequence of internal magnets as sub-arrays
seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1],
       ]

#Define function to power stepper motor
def run():
    #This for loop commands the small wheel attached to the stepper motor to turn a number of degrees
    #For example
    #128 is a quarter turn
    #512 is a full turn
    #1024 is two full turns
    for i in range(8):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], seq[halfstep][pin])
            time.sleep(0.001)
            
#Run a function to do nothing to get motor to stop
def stop():
    print("Motor stopped")
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#Set up pin for buzzer XXXXX
GPIO.setup(18, GPIO.OUT)
#XXXXXXXXXXXXXXXXXXXXXXXXXXX

def writeCSV():
    f = open('/home/pi/Desktop/csv_file.txt', 'w')
    writer = csv.writer(f)
    title = ["EVENT LOG"]
    header = ["Type of event", "Time"]
    row = ["row"]        
    writer.writerow(title)
    writer.writerow(header)
    writer.writerow(stringArray)
    print(stringArray)


#Define on connect function for MQTT
def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
      
    else:
        print("Connection failed")

#Keep movement alerts stored as an array of strings
stringArray = []

#Define on_message function for MQTT
def on_message(client, userdata, message):

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    if b'activate buzzer' in message.payload:
        print ("ALERT!!! Zonescanner has been moved!!   " + date_time)
        stringArray.append('Movement alarm raised at ' + date_time + '\r')
        GPIO.output(18, True)
    
    elif b'stop motor' in message.payload:
        print("MOTOR STOPPED")
        stop()
        
    elif b'cancel buzzer' in message.payload:
        print("Zonescanner is in correct position")
        GPIO.output(18, False)
        
    elif b'start motor' in message.payload:
        print("Motor started")
        run()        
Connected = False

#Details of broker on sink
mqttBroker ="192.168.8.115"
brokerPort = 1883
client = mqttClient.Client("Buzzer")
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback
client.connect(mqttBroker,brokerPort)
client.loop_start()        #start the loop
client.subscribe("Alarm")


while Connected != True:    #Wait for connection
    time.sleep(0.1)
    
try:
    while True:
        time.sleep(1)


  
except KeyboardInterrupt:
    print ("Connection terminated by user")
    writeCSV()
    client.disconnect()
    client.loop_stop()


#Reset GPIO pins at end
GPIO.cleanup()
