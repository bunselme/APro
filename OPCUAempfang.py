#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import thread
from opcua import Server

#Einstllung für GPIOs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,True)     #Grundstellung


  
    
print "versuche OPCUA Server zu starten....Geduld, dieses dauert einige Sekunden"
server=Server()
 
url= "opc.tcp://192.168.1.21:4840"

server.set_endpoint(url)

name="OPCUA_Roboter_SERVER"

addspace =server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")


#Startrigger für Fraesprozess
Start  = Param.add_variable(addspace, "Trigger_Prozessstart", False)
Start.set_writable()
server.start()
    
print("OPCUA Server wurde erfolgreich gestartet und sendet alle 0.1 Sekunden Sensordaten")
print("Server startet at {}".format(url))

while True: 

        starttrigger=Start.get_value() 
        
        if starttrigger == True:
            GPIO.output(4,False)
            print "Roboter fährt----------------------"
        if starttrigger == False:
            GPIO.output(4,True)
            print "Roboter stoppt"

            
        time.sleep(0.1) #Prozessorlast reduzieren


        
       
