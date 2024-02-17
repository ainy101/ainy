import math
from adafruit_servokit import ServoKit

import board
import busio

i2c_bus0= busio.I2C(board.SCL_1, board.SDA_1)
kit= ServoKit(channels=16,i2c= i2c_bus0 )

xx = 28
yy = 5
L1 = 10.5
L2 = 10

x= -(0.078*xx )+ 43.18
x = 10
y= -(0.09*yy)+40.5

C2 = (pow(x,2) + pow(y,2) - pow(L1,2) - pow(L2,2))/(2*L1*L2)
S2 = math.sqrt(pow(C2,2)-1)
T2 = math.atan2(S2,C2)
K1 = L1+ L2*C2
K2 = L2*S2
R = math.sqrt(pow(K1,2)+pow(K2,2))
Gamma = math.atan2(K2,K1)
K1 = R*(math.cos(Gamma))
K2 = R*(math.sin(Gamma))
T1 =  math.atan2(K2,K1)- math.atan2(y,x) 
TD1 = (360*T1)/(2*3.14)
TD2 = (360*T2)/(2*3.14)
TD1 = int(TD1)
TD1 = 180-TD1
TD2 = int(TD2)
TD2 = 180-TD2
print(TD1)
print(TD2)

kit.servo[0].angle = 20


kit.servo[1].angle = abs(TD1)

#kit.servo[2].angle = abs(TD2)