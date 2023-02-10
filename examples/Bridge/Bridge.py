################################################################################
# SMW-SX1262M0 Bridge (v1.0)
#
# Simple program to bridge the computer to the LoRaWAN module.
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
import serial

response = "" # to store the module's responses

serialConnection = serial.Serial("/dev/serial0", baudrate=9600) # serial connection

# main program

print("--- SMW-SX1262M0 Bridge ---")

while True:
    # ask for user input
    command = input("Write your command: ")
    if command == "exit":
        print("Bye")
        break

    # send input to the module
    serialConnection.write(f"{command}\n".encode())
    response = "" # erase the variable
    sleep(1) # 1 [s]

    # read buffer
    while serialConnection.inWaiting():
        buffer = serialConnection.read(serialConnection.inWaiting())
        sleep(0.1) # 100 [ms]
        response += (buffer.decode(encoding="utf8", errors='ignore')) # converts the answer to UTF-8

    # print the answer
    print(response)
