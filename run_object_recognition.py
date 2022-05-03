import cv2
import os
import csv

#Modified code is surrounded by xxxxxxxxxxxxxxxx

#xxxxxxxxxxxxxxxxxxxxxx
from datetime import datetime

stringArray = []

def writeCSV():
    f = open('/home/pi/Desktop/AI_images/report/csv_file.txt', 'w')
    writer = csv.writer(f)
    title = ["EVENT LOG"]
    header = ["Type of event", "Time"]
    row = ["row"]        
    writer.writerow(title)
    writer.writerow(header)
    writer.writerow(stringArray)
    print(stringArray)
#xxxxxxxxxxxxxxxxxxxxxx

#classFile is link to coco.names
classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"

#coco.names is opened as classFile
with open(classFile,"rt") as f:
    
    classNames = f.read().rstrip("\n").split("\n")

#This is to pull the information about what each object should look like
configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

#This is some set up values to get good results
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#This is to set up what the drawn box size/colour is and the font/size/colour of the name tag and confidence label   
def getObjects(img, thres, nms, draw=True, objects=[]):
    
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)

    if len(objects) == 0: objects = classNames
    
    objectInfo =[]
    
    if len(classIds) != 0:
        
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            
            className = classNames[classId - 1]
            
            if className in objects:
                
                objectInfo.append([box,className])
                
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10, box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200, box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)                    
                    
                    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    outputString= ""
                    outputString = className
                    logString =""
                
                    if outputString == "person":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        logString = "A person was detected at: " + dtString

                        stringArray.append('Person detected at: ' + dtString + '\r')

                        savePersonImage = "/home/pi/Desktop/AI_images/people/person_"+ dtString +".jpg"
                        outputImage = cv2.imwrite(savePersonImage, img)
                        print(logString)
                
                    elif outputString == "dog":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        logString = "A dog was detected at: " + dtString

                        stringArray.append('Dog detected at: ' + dtString + '\r')
                        
                        saveDogImage = "/home/pi/Desktop/AI_images/dogs/dog"+ dtString +".jpg"
                        outputImage = cv2.imwrite(saveDogImage, img)
                        print(logString)
                        
                    elif outputString == "car":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        
                        saveCarVanImage = "/home/pi/Desktop/AI_images/cars_and_vans/vehicle_"+ dtString +".jpg"
                        logString = "A car (or van) was detected at: " + dtString
                        outputImage = cv2.imwrite(saveCarVanImage, img)
                        print(logString)
                        
                    elif outputString == "motorcycle":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        
                        saveMotorcycleImage = "/home/pi/Desktop/AI_images/motorcycle/motorcycle"+ dtString +".jpg"
                        logString = "A motorcycle was detected at: " + dtString
                        outputImage = cv2.imwrite(saveMotorcycleImage, img)
                        print(logString)
                        
                    elif outputString == "bus":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        
                        saveBusImage = "/home/pi/Desktop/AI_images/bus/bus_"+ dtString +".jpg"
                        logString = "A bus was detected at: " + dtString
                        outputImage = cv2.imwrite(saveBusImage, img)
                        print(logString)
                        
                    elif outputString == "truck":
                        dt = datetime.now()
                        dtString = dt.strftime("%d-%b-%Y (%H:%M:%S)")
                        
                        saveTruckImage = "/home/pi/Desktop/AI_images/truck/truck"+ dtString +".jpg"
                        logString = "A truck was detected at: " + dtString
                        outputImage = cv2.imwrite(saveTruckImage, img)
                        print(logString)
                        
                    #Note: vans are detected as cars!

                    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



    return img,objectInfo

#Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,960)
    #cap.set(10,70)
    
    #Below is the never ending loop that determines what will happen when an object is identified.
    
    #Create array for storing all CV2 image data as strings which can be sent to sink pi
    outputArray = []
    
    count = 0
    
    #Modify this line to determine how long the image recognition and capture should run
    while count <= 100:

        success, img = cap.read()


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        outputArray.append(img)
        
        #Below provides a huge amount of control. the 0.45 number is the threshold number, the 0.2 number is the nms number)
        
        result, objectInfo = getObjects(img,0.6,0.2)
    
        #Uncomment here to see image recognition in action
        #This runs better on an RPi with this turned off!!!!
        #cv2.imshow("Output",img)
        #cv2.waitKey(1)

        count = count + 1
    
#End the automated detection and close pop-up window
cv2.destroyAllWindows()

#Check the number of images that have been collected - should be the same as the number of times a relevant object has been detected
print(len(outputArray))

#Write CSV file into AI_images folder for sending to sinkPi
writeCSV()

#Run Terminal command from this script sending all of the photographs and the log report to the sinkPi over SSH
#via a connection protected by a recognised host key
os.system('scp -r /home/pi/Desktop/AI_images pi@192.168.8.115:/home/pi/Desktop')



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
