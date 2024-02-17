from adafruit_servokit import ServoKit

import time
import board
import busio

i2c_bus0= busio.I2C(board.SCL_1, board.SDA_1)
kit= ServoKit(channels=16,i2c= i2c_bus0 )

  
kit.servo[0].angle = 130

kit.servo[1].angle = 170

kit.servo[2].angle = 20

kit.servo[3].angle =  130

kit.servo[4].angle =  0

kit.servo[5].angle =  20

#Pick 
                                                          

for i in range(130,30,-1):
       kit.servo[0].angle= i


for i in range(170,100,-1):
       kit.servo[1].angle= i
       time.sleep(.01)

time.sleep(.51)

for i in range(20,56,1):
       kit.servo[5].angle= i
       time.sleep(.01)
time.sleep(.51)

#place
for i in range(100,170,1):
       kit.servo[1].angle= i
       time.sleep(.01)

                                                          
for i in range(30,130,1):
       kit.servo[0].angle= i
       time.sleep(.01)

 #SORTING AFTER PICKNG

for i in range(170,100,-1):
       kit.servo[1].angle= i
       time.sleep(.01)

for i in range(53,20,-1):
       kit.servo[5].angle= i
       time.sleep(.01)
       
for i in range(100,170,1):
       kit.servo[1].angle= i
       time.sleep(.01)
