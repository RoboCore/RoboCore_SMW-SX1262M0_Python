######################################################################################
# SMW-SX1262M0 Simple Receive - ABP (v1.0)
#
# This program was created with the purpose of showing a simple example 
# of receiving data through the ABP mode
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

DEVADDR = "00000000"
APPSKEY = "00000000000000000000000000000000"
NWKSKEY = "00000000000000000000000000000000"
MODE_ABP = 0 # 0 = ABP / 1 = OTAA
PAUSE_TIME = 300000 # [ms] (5 min)

joined = False
lorawan = SMW_SX1262M0("/dev/serial0")

# main program

print("--- SMW-SX1262M0 Downlink (ABP) ---")

# reset the module
lorawan.reset()

# set join mode to ABP
returnCode = lorawan.set_JoinMode(MODE_ABP)
if returnCode == CommandResponse.OK:
    print("Mode set to ABP")
else:
    print("Error setting the join mode")

# read the Device EUI
returnCode, response = lorawan.get_DevEUI()
if returnCode == CommandResponse.OK:
    print(f"DevEUI: {response}")
else:
    print("Error getting the Device EUI")

# set the Device Address
returnCode = lorawan.set_DevAddr(DEVADDR)
if returnCode == CommandResponse.OK:
    print(f"Device Address set {DEVADDR}")
else:
    print("Error setting the Device Address")

# set the Application Session Key
returnCode = lorawan.set_AppSKey(APPSKEY)
if returnCode == CommandResponse.OK:
    print(f"Application Session Key set {APPSKEY}")
else:
    print("Error setting the Application Session Key")

# set the Network Session Key
returnCode = lorawan.set_NwkSKey(NWKSKEY)
if returnCode == CommandResponse.OK:
    print(f"Network Session Key set {NWKSKEY}")
else:
    print("Error setting the Network Session Key")

# save the current configuration (optional)
returnCode = lorawan.save()
if returnCode == CommandResponse.OK:
    print("Settings saved")
else:
    print("Error on saving")

# join the network (not really necessary in ABP)
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
                sleep(10) # 10 [s]
                # read the message received (text data)
                returnCode, port, response = lorawan.readT()
                if returnCode == CommandResponse.OK:
                    # check if a downlink was received
                    if response:
                        print(f"Port: {port} Message: {response}")
                    else:
                        print("No message received")
                else:
                    print("Error receiving message")
            else:
                print("Error sending the message")

            # update the timeout
            timeout = lorawan.millis() + PAUSE_TIME
        else:
            # show some activity
            print(".")
            # update the timeout
            timeout = lorawan.millis() + 5000 # [ms] (5 s)
