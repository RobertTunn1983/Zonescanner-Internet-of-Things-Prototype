#MQTT
import paho.mqtt.client as mqtt 
mqttBroker ="192.168.8.115"
brokerPort = 1883
client = mqtt.Client()
client.connect(mqttBroker,brokerPort)

#Import time
import time

#Sense Hat
from sense_hat import SenseHat
sense = SenseHat()

#Infinite loop to take accelerometer readings 
while True:
    #Get the acceleration reading
    accel = sense.get_accelerometer_raw()
    #Take reading every half second or too much data is produced
    #and the run function on in combined_buzzer_motor code will run too long
    #for this same reason an infinite loop to operate motor does not work
    time.sleep(0.5)
    x = accel['x']
    y = accel['y']
    z = accel['z']
    
    #Parse these values as floats and round down, degree of sensitivity can be altered by
    #changing the number of decimal places
    x = float(round(x,1))
    y = float(round(y,1))
    z = float(round(z,1))    
    
    #Normal position for RPi is x=0, y=0, z=1
    #Uncomment to check
    print(f"x={x}, y={y}, z={z}")

    #Set up boolean flag variable
    flag = True
    
    #If position of Zonescanner moves, activate alarm
    if x != 0.0 or y != 0.0 or z != 1.0:
        flag = True
    #If it returns to original position, cancel alarm
    elif x == 0.0 and y == 0.0 and z == 1.0:
        #client.publish(topic="Alarm", payload="start motor")
        flag = False
    
    if flag == True:
        print("Zonescanner moved")
        client.publish(topic="Alarm", payload="stop motor")
        client.publish(topic="Alarm", payload="activate buzzer")
    elif flag == False:
        print("Zonescanner in correct position")
        client.publish(topic="Alarm", payload="cancel buzzer")
        client.publish(topic="Alarm", payload="start motor")
