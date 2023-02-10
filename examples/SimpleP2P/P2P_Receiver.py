######################################################################################
# SMW-SX1262M0 P2P Receiver (v1.0)
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
TIMEOUT_LISTEN = 1000 # to avoid errors, use at least 1000 millis of timeout (1 s)

lorawan = SMW_SX1262M0("/dev/serial0")

# main program

print("--- SMW-SX1262M0 P2P Receiver ---")

returnCode = lorawan.P2P_start(frequency=FREQUENCY, continuous=CONTINUOUS_MODE)

if returnCode == CommandResponse.OK:
    print("Listening...\n")

    # check if CONTINUOUS_MODE is true
    if CONTINUOUS_MODE:
        print("Press Ctrl + C to terminate.")
        # this loop will only end if you press Ctrl+C
        while True:
            try:
                # listen for incoming data
                receivedData = lorawan.P2P_listen(TIMEOUT_LISTEN)
                # check the message
                if receivedData:
                    message, rssi, snr = receivedData # separate the received data
                    print(f"RSSI={rssi}")
                    print(f"SNR={snr}")
                    print(f"Message received: {message}\n")
            except KeyboardInterrupt:
                print("Bye")
                break

    else:
        # listen for incoming data
        receivedData = lorawan.P2P_listen(TIMEOUT_LISTEN)
        # check the message
        if receivedData:
            message, rssi, snr = receivedData # separate the received data
            print(f"RSSI={rssi}")
            print(f"SNR={snr}")
            print(f"Message received: {message}\n")

else:
    print("Error")

# stop the receiver
lorawan.P2P_stop()
