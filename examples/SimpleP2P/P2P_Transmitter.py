######################################################################################
# SMW-SX1262M0 P2P Transmitter (v1.0)
# 
# This program was created with the purpose of showing an example of
# peer-to-peer (P2P) communication between two LoRaWAN modules.
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

from time import sleep
from RoboCore_SMW_SX1262M0 import SMW_SX1262M0, CommandResponse

# variables

CONTINUOUS_MODE = False # "True" to set the continuous mode
FREQUENCY = 915200

lorawan = SMW_SX1262M0("/dev/serial0")

# main program

print("--- SMW-SX1262M0 P2P Transmitter ---")

returnCode = lorawan.P2P_start(frequency=FREQUENCY, continuous=CONTINUOUS_MODE, message="Hello World")

if returnCode == CommandResponse.OK:
    print("Message sent successfully")

    # check if CONTINUOUS_MODE is true
    if CONTINUOUS_MODE:
        # wait for user interaction to continue code execution 
        input('Press Enter to stop sending') 

    print("Bye")

else:
    print("Error sending the message")

# wait some time for the module to effectively send the message
sleep(1)

# stop the transmitter
lorawan.P2P_stop()
