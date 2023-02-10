######################################################################################
# SMW-SX1262M0 Simple Send - OTAA (v1.0)
#
# This program was created with the purpose of showing a simple example of 
# sending data through OTAA mode.
#
# Copyright 2023 RoboCore.
# Written by Luan.f (06/02/2023).
#
#
# This file is part of the SMW-SX1262M0 library ("SMW-SX1262M0-lib").
#
# "SMW-SX1262M0-lib" is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "SMW-SX1262M0-lib" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with "SMW-SX1262M0-lib". If not, see <https://www.gnu.org/licenses/>
######################################################################################

# libraries

from RoboCore_SMW_SX1262M0 import SMW_SX1262M0, CommandResponse
from time import sleep

# variables

APPEUI = "0000000000000000" 
APPKEY = "00000000000000000000000000000000" 
MODE_OTAA = 1 # 0 = ABP / 1 = OTAA
PAUSE_TIME = 300000 # [ms] (5 min)

joined = False
lorawan = SMW_SX1262M0("/dev/serial0")

# main program

print("--- SMW-SX1262M0 Join (OTAA) ---")

# reset the module
lorawan.reset()

# set join mode to OTAA
returnCode = lorawan.set_JoinMode(MODE_OTAA)
if returnCode == CommandResponse.OK:
    print("Mode set to OTAA")
else:
    print("Error setting the join mode")

# read the Device EUI
returnCode, response = lorawan.get_DevEUI()
if returnCode == CommandResponse.OK:
    print(f"DevEUI: {response}")
else:
    print("Error getting the Device EUI")

# set the Application EUI
returnCode = lorawan.set_AppEUI(APPEUI)
if returnCode == CommandResponse.OK:
    print(f"Application EUI set {APPEUI}")
else:
    print(f"Error setting the Application EUI")

# set the Application Key
returnCode = lorawan.set_AppKey(APPKEY)
if returnCode == CommandResponse.OK:
    print(f"Application Key set {APPKEY}")
else:
    print(f"Error stting the Application Key")

# save the current configuration (optional)
returnCode = lorawan.save()
if returnCode == CommandResponse.OK:
    print("Settings saved")
else:
    print("Error on saving")

# join the network
print("Joining the network")
lorawan.join()

# get the current time [ms]
timeout = lorawan.millis()

while True:
    if lorawan.millis() > timeout:
        # check if connected
        if lorawan.isConnected():
            # print the "joined" message
            if not joined:
                print("Joined")
                joined = True

            # send the message (text data)
            returnCode = lorawan.sendT(12, "Hello World!")
            if returnCode == CommandResponse.OK:
                print("Message sent")

            # update the timeout
            timeout = lorawan.millis() + PAUSE_TIME
        else:
            # show some activity
            print(".")
            # update the timeout
            timeout = lorawan.millis() + 5000 # (5 s)
