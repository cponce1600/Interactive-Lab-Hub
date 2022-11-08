import time
import board
import busio
import adafruit_mpr121
import qwiic
import sys
import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/here'

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

print("VL53L1X Qwiic Test\n")
ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor online!\n")

while True:
    for i in range(12):
        if mpr121[i].value:
            ToF.start_ranging()
            time.sleep(.05)
            distance = ToF.get_distance()
            time.sleep(.05)
            ToF.stop_ranging()
            
            fe = (distance / 25.4)/ 12.0
            val = f"feet away: {fe}!"

            print(val)
            client.publish(topic, val)
    time.sleep(0.25)
