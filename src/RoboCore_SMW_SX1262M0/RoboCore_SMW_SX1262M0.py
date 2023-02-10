#################################################################################################################

# RoboCore SMW-SX1262M0 Library (Python) (v1.0)

# Library to use the SMW-SX1262M0 LoRaWAN module.

# Copyright 2023 RoboCore.
# Written by Luan.f (06/02/2023).


# This file is part of the SMW-SX1262M0 library ("SMW-SX1262M0-lib").

# "SMW-SX1262M0-lib" is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# "SMW-SX1262M0-lib" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with "SMW-SX1262M0-lib". If not, see <https://www.gnu.org/licenses/>

#################################################################################################################

# Necessary libraries
import serial
import string
from enum import IntEnum
from time import monotonic


class CommandResponse(IntEnum):
    """This class is used as enumeration (enum)."""

    OK = 0  # command run correctly without error
    AT_ERROR = 101  # generic AT error
    AT_BUSY_ERROR = 102  # the LoRa network is busy, so the AT command has not been completed
    AT_PARAM_ERROR = 103  # a parameter of the AT command is wrong
    AT_TEST_PARAM_OVERFLOW = 104  # the parameter of the AT command is too long
    AT_NO_NETWORK_JOINED = 105  # the LoRa network has not been joined yet
    PARAM_ERROR = 200  # a parameter of the function is wrong


class SMW_SX1262M0:
    """This class was created to facilitate the use of the SMW-SX1262M0 LoRaWAN module 
    (uses some native python 3.9.2 libraries)."""

    SMW_SX1262M0_TIMEOUT_READ = 100  # [ms]
    SMW_SX1262M0_TIMEOUT_WRITE = 500  # [ms]
    SMW_SX1262M0_TIMEOUT_RESET = 3000  # [ms]

    # command dictionary (AT v2.14)
    __commandDictionary = {

        "CMD_AT": "AT",  # AT (3.1.1)
        "CMD_APPEUI": "APPEUI",  # Application EUI (3.2.1)
        "CMD_APPKEY": "APPKEY",  # Application Key (3.2.1)
        "CMD_APPSKEY": "APPSKEY",  # Application Session Key (3.2.3)
        "CMD_DADDR": "DADDR",  # Device Address (3.2.4)
        "CMD_DEVEUI": "DEUI",  # Device EUI (3.2.5)
        "CMD_NWKID": "NWKID",  # Network ID (3.2.6)
        "CMD_NWKSKEY": "NWKSKEY",  # Network Session Key (3.2.7)
        "CMD_CFM": "CFM",  # Confirm Mode (3.3.1)
        "CMD_CFS": "CFS",  # Confirm Status (3.3.2)
        "CMD_JOIN": "JOIN",  # Join (3.3.3)
        "CMD_NJM": "NJM",  # Join Mode (3.3.4)
        "CMD_NJS": "NJS",  # Join Status (3.3.5)
        "CMD_RECV": "RECV",  # Receive (3.3.6)
        "CMD_RECVB": "RECVB",  # Receive - Binary (3.3.7)
        "CMD_SEND": "SEND",  # Send (3.3.8)
        "CMD_SENDB": "SENDB",  # Send - Binary (3.3.9)
        "CMD_ADR": "ADR",  # Adaptive Data Rate (3.4.1)
        "CMD_CLASS": "CLASS",  # LoRaWAN Class (3.4.2)
        "CMD_DR": "DR",  # Data Rate (3.4.4)
        "CMD_TXP": "TXP",  # Transmit Power (3.4.12)
        "CMD_RSSI": "RSSI",  # RSSI (3.7.1)
        "CMD_SNR": "SNR",  # SNR (3.7.2)
        "CMD_VERSION": "VER",  # Version (3.7.4)
        "CMD_LORA_TX": "TXLRA",  # TX LoRa Test (3.8.1)
        "CMD_LORA_RX": "RXLRA",  # RX LoRa Test (3.8.4)
        "CMD_LORA_CONFIG": "TCONF",  # Configuration of LoRa Test (3.8.5)
        "CMD_LORA_OFF": "TOFF",  # Stop LoRa Test (3.8.6)
        "CMD_SAVE": "SAVE",  # Save configuration (3.10.1)
        "CMD_AJOIN": "AJOIN",  # Automatic Join (3.10.3)

    }

    # dictionary of actions
    __commandAction = {

        "RUN": "",  # used to send the command
        "GET": "=?",  # used to get the command configuration
        "SET": "=",  # used to configure a command
        "HELP": "?",  # used to know the possible use of the command

    }

    # this variable contains the P2P message
    __messageReceived = ""

    def __init__(self, port, timeout=None):
        """This method is the constructor of the class.

        :param port [str]: the serial port that will be used to communicate with the module
        :param timeout [int]: the time the port will wait for the module to respond (default = None)
        """

        self.__port = port
        self.__timeout = timeout
        self.__serialConnection = serial.Serial(
            port=self.__port, baudrate=9600, timeout=self.__timeout)

    def millis(self):
        """This method gets the time in ms.
        
        :return: the value [int] 
        """

        return round(monotonic() * 1000)

    def flush(self):
        """This method clears the serial buffer."""

        self.__serialConnection.flushInput()

    def get_ADR(self):
        """This method gets the Adaptive Data Rate.

        :return: the response of the command [CommandResponse] and the value [int]
        """

        # send the command and read the response
        self.__sendCommand("CMD_ADR", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_Ajoin(self):
        """This method gets the Automatic Join.

        :return: the response of the command [CommandResponse] and the value [int] 
        """

        # send the command and read the response
        self.__sendCommand("CMD_AJOIN", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_AppEUI(self):
        """This method gets the Application EUI.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_APPEUI", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_AppKey(self):
        """This method gets the Application Key.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_APPKEY", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_AppSKey(self):
        """This method gets the Application Session Key.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_APPSKEY", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_DevAddr(self):
        """This method gets the Device Address.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_DADDR", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_DevEUI(self):
        """This method gets the Device EUI.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_DEVEUI", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_DR(self):
        """This method gets the Data Rate.

        :return: the response of the command [CommandResponse] and the value [int]
        """

        # send the command and read the response
        self.__sendCommand("CMD_DR", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_JoinMode(self):
        """This method gets the Network Join Mode.

        :return: the response of the command [CommandResponse] and the value [int] 
        """

        # send the command and read the response
        self.__sendCommand("CMD_NJM", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_JoinStatus(self):
        """This method gets the Join Status.

        :return: the response of the command [CommandResponse] and the value [int]
        """

        # send the command and read the response
        self.__sendCommand("CMD_NJS", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response[-1])

        return (CommandResponse[statusCommand], res)

    def get_NwkSKey(self):
        """This method gets the Network Session Key.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_NWKSKEY", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_RSSI(self):
        """This method gets the RSSI of the last received message.

        :return: the response of the command [CommandResponse] and the value [int]
        """

        # send the command and read the response
        self.__sendCommand("CMD_RSSI", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_SNR(self):
        """This method gets the SNR of the last received message.

        :return: the response of the command [CommandResponse] and the value [int]
        """

        # send the command and read the response
        self.__sendCommand("CMD_SNR", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = int(response) if response else None

        return (CommandResponse[statusCommand], res)

    def get_Version(self):
        """This method gets the firmware version of the module.

        :return: the response of the command [CommandResponse] and the value [str]
        """

        # send the command and read the response
        self.__sendCommand("CMD_VERSION", "GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        res = str(response) if response else None

        return (CommandResponse[statusCommand], res)

    def isConnected(self):
        """This method checks if the module is connected to the network.

        :return: the response of the command [bool]
        """

        # check connection status (0 or 1)
        res = self.get_JoinStatus()[-1] # get only the value (0 or 1)
        if res == 1:
            return True
        else:
            return False

    def join(self):
        """This method starts a join to the network.

        :return: the response of the command [CommandResponse]
        """

        # send the command and read the response
        self.__sendCommand("CMD_JOIN", "RUN")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def P2P_listen(self, timeout_listen):
        """This method listens for incoming P2P messages.

        :param timeout_listen [int]: the time to wait, in [ms]

        :return: message [str], RSSI [int] and SNR [int] if a message was received 
        or False [bool] otherwise
        """

        statusMessage = False
        timeout = self.millis() + timeout_listen  # [ms]
        while self.millis() < timeout:
            buffer = self.__serialConnection.read(
                self.__serialConnection.inWaiting())

            if buffer:
                # convert the response to UTF-8
                self.__messageReceived += (buffer.decode(encoding="utf8",
                                                         errors='ignore'))

            # check if the message has ended
            elif "\n\r" in self.__messageReceived or "Test Stop" in self.__messageReceived:
                statusMessage = True
                break

        # check if the message is True
        if statusMessage:

            try:
                # parse the message
                res = self.__messageReceived.replace("Test Stop", "")
                # get the message
                message = (res.split("Text-> ")[-1]).strip()
                # get the RSSI and the SNR
                res = res.split()
                for word in res:
                    if "RSSI=" in word:
                        rssi = word.split("RSSI=")[-1]
                    elif "SNR=" in word:
                        snr = word.split("SNR=")[-1]

                self.__messageReceived = "" # clear the variable
                self.flush()

                return str(message), int(rssi), int(snr)

            except:
                return False

        else:
            return False

    def P2P_start(self, frequency=915200, continuous=False, message=None):
        """This method configures the module for a P2P communication.

        :param frequency [int]: the frequency to use for the wireless communication, in [kHz]
        :param continuous [bool]: True to make the communication persistent
        :param message [str]: the message to be sent or None to set as receiver (default = None)

        :return: the response of the command [CommandResponse]

        Note: upon transmission, the module might need some time to effectively send the message 
        after the command has been executed.
        """

        # send the command and read the response

        mode = 1 if continuous else 0 # check which mode was selected

        # if message is None, the module will be set as receiver
        if message is None:
            param = f"{frequency}:{mode}"
            self.__sendCommand("CMD_LORA_RX", "SET", param)

        else:
            param = f"{frequency}:{mode}:{message}"
            self.__sendCommand("CMD_LORA_TX", "SET", param)

        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()

        return (CommandResponse[statusCommand])

    def P2P_stop(self):
        """This method stops the P2P communication.

        :return: the response of the command [CommandResponse]
        """

        # send the command and read the response
        self.__sendCommand("CMD_LORA_OFF", "RUN")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def ping(self):
        """This method pings the module.

        :return: the response of the command [CommandResponse]
        """

        # send the command and read the response
        self.__sendCommand(cmd="", action="RUN")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def readT(self):
        """This method reads a text message from the module.

        :return: the response of the command [CommandResponse], the port [int] and the message [str]
        """

        # send the command and read the response
        self.__sendCommand(cmd="CMD_RECV", action="GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        # the first split is used to ignore asynchronous events (chapter 3.6 of AT command set V0.1_Rev2.14)
        port, message = response.split()[-1].split(":")

        return (CommandResponse[statusCommand], int(port), str(message))

    def readX(self):
        """This method reads a hexadecimal message from the module.

        :return: the response of the command [CommandResponse], the port [int] and the message [str]
        """

        # send the command and read the response
        self.__sendCommand(cmd="CMD_RECVB", action="GET")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]
        response = response.split(statusCommand)[0].strip()
        # the first split is used to ignore asynchronous events (chapter 3.6 of AT command set V0.1_Rev2.14)
        port, message = response.split()[-1].split(":")

        return (CommandResponse[statusCommand], int(port), str(message))

    def reset(self):
        """This method resets the module."""

        # send the command and read the response
        self.__serialConnection.write("ATZ\n".encode())
        self.__readCommand(self.SMW_SX1262M0_TIMEOUT_RESET)

    def save(self):
        """This method saves the module's configuration."""

        # send the command and read the response
        self.__sendCommand("CMD_SAVE", "RUN")
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def sendT(self, port, message):
        """This method sends a text message.

        :param port [int]: the port to send the message
        :param message [str]: the message to send

        :return: the response of the command [CommandResponse]
        """

        param = f"{port}:{message}"

        # send the command and read the response
        self.__sendCommand("CMD_SEND", "SET", param)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def sendX(self, port, message):
        """This method sends a hexadecimal message.

        :param port [int]: the port to send the message
        :param message [str]: the message to send

        :return: the response of the command [CommandResponse]
        """

        # ensure there is no space in the message
        message = message.replace(" ", "")

        # check if the message is hexadecimal

        if all(c in string.hexdigits for c in message):

            param = f"{port}:{message}"

            # send the command and read the response
            self.__sendCommand("CMD_SENDB", "SET", param)
            response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
            # parse the response
            statusCommand = response.split()[-1]

            return (CommandResponse[statusCommand])

        else:
            return (CommandResponse["PARAM_ERROR"])

    def set_ADR(self, adr):
        """This method sets the Adaptive Data Rate.

        :param adr [int]: the value for the Adaptive Data Rate (0 or 1)

        :return: the response of the command [CommandResponse]
        """

        # check if the value passed is within the range
        if adr > 1:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_ADR", "SET", adr)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_AJoin(self, mode):
        """This method sets the Automatic Join.

        :param mode [int]: the value for the mode (0 or 1) 

        :return: the response of the command [CommandResponse]
        """

        # check if the value passed is within the range
        if mode > 1:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_AJOIN", "SET", mode)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_READ)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_AppEUI(self, appEui):
        """This method sets the Application EUI.

        :param appEui [str]: the value for the Application EUI

        :return: the response of the command [CommandResponse]
        """

        # check if the key is already in the correct pattern
        if ":" in appEui and len(appEui) == 23:
            pass

        # format the string ("xx:xx:xx:xx:xx:xx:xx:xx")
        elif len(appEui) == 16:
            numberAppEui = ""
            for i in range(0, 16, 2):
                if i == 14:
                    numberAppEui += appEui[i] + appEui[i+1]
                    break
                else:
                    numberAppEui += appEui[i] + appEui[i+1] + ":"
                    pass
            appEui = numberAppEui
        else:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_APPEUI", "SET", appEui)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_AppKey(self, key):
        """This method sets the Application Key.

        :param key [str]: the value for the Application Key

        :return: the response of the command [CommandResponse]
        """

        # check if the key is already in the correct pattern
        if ":" in key and len(key) == 47:
            pass

        # format the string ("xx:xx:xx:xx:xx:xx:xx:xx")
        elif len(key) == 32:
            numberKey = ""
            for i in range(0, 32, 2):
                if i == 30:
                    numberKey += key[i] + key[i+1]
                    break
                else:
                    numberKey += key[i] + key[i+1] + ":"

            key = numberKey
        else:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_APPKEY", "SET", key)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_AppSKey(self, skey):
        """This method sets the Application Session Key.

        :param skey [str]: the value for the Application Session Key

        :return: the response of the command [CommandResponse]
        """

        # check if the key is already in the correct pattern
        if ":" in skey and len(skey) == 47:
            pass

        # format the string ("xx:xx:xx:xx:xx:xx:xx:xx")
        elif len(skey) == 32:
            numberSKey = ""
            for i in range(0, 32, 2):
                if i == 30:
                    numberSKey += skey[i] + skey[i+1]
                    break
                else:
                    numberSKey += skey[i] + skey[i+1] + ":"

            skey = numberSKey
        else:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_APPSKEY", "SET", skey)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_DevAddr(self, devAddr):
        """This method sets the Device Address.

        :param devAddr [str]: the value for the Device Address

        :return: the response of the command [CommandResponse]
        """

        # check if the key is already in the correct pattern
        if ":" in devAddr and len(devAddr) == 11:
            pass

        # format the string ("xx:xx:xx:xx")
        elif len(devAddr) == 8:
            numberDevAddr = ""
            for i in range(0, 8, 2):
                if i == 6:
                    numberDevAddr += devAddr[i] + devAddr[i+1]
                    break
                else:
                    numberDevAddr += devAddr[i] + devAddr[i+1] + ":"
                    pass
            devAddr = numberDevAddr
        else:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_DADDR", "SET", devAddr)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_DR(self, dr):
        """This method sets the Data Rate.

        :param dr [int]: the value for the Data Rate (0-6 corresponding to DR_X)

        :return: the response of the command [CommandResponse]
        """

        # check if the passed value is within the range
        if dr > 6:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_DR", "SET", dr)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_JoinMode(self, mode):
        """This method sets the Network Join Mode.

        :param mode [int]: the value for the mode (0 or 1)

        :return: the response of the command [CommandResponse]
        """

        # check if the value passed is within the range
        if mode > 1:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_NJM", "SET", mode)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def set_NwkSKey(self, nwkSKey):
        """This method sets the Network Session Key.

        :param nwkSKey [str]: the value for the Network Session Key

        :return: the response of the command [CommandResponse]
        """

        # check if the key is already in the correct pattern
        if ":" in nwkSKey and len(nwkSKey) == 47:
            pass

        # format the string ("xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx")
        elif len(nwkSKey) == 32:
            numberNwkSKey = ""
            for i in range(0, 32, 2):
                if i == 30:
                    numberNwkSKey += nwkSKey[i] + nwkSKey[i+1]
                    break
                else:
                    numberNwkSKey += nwkSKey[i] + nwkSKey[i+1] + ":"
                    pass
            nwkSKey = numberNwkSKey
        else:
            return (CommandResponse["PARAM_ERROR"])

        # send the command and read the response
        self.__sendCommand("CMD_NWKSKEY", "SET", nwkSKey)
        response = self.__readCommand(self.SMW_SX1262M0_TIMEOUT_WRITE)
        # parse the response
        statusCommand = response.split()[-1]

        return (CommandResponse[statusCommand])

    def __sendCommand(self, cmd, action, parameter=""):
        """This method uses the serial connection to send commands to the module.

        :param cmd [str]: the command to be sent
        :param action [str]: the action for the command (RUN, GET, SET, HELP)
        :param parameter: can be [int] or [str] 
        (depends on the command that will be sent to the module)

        Example: [AT+NJM]  [=]     [1] 
                   cmd   action  parameter
        """

        if cmd:
            finalCommand = f"AT+{self.__commandDictionary[cmd]}{self.__commandAction[action]}{parameter}"

        else:
            finalCommand = f"AT{self.__commandAction[action]}"

        # it is IMPORTANT not to use '\r' and '\n' together
        # self.flush()
        self.__serialConnection.write(f"{finalCommand}\n".encode())

    def __readCommand(self, timeout):
        """This method reads the response of a command.

        :param timeout [int]: the time to wait, in [ms]

        :return: the module's response to the command sent [str]
        """

        response = ""
        stop = False
        timeout = self.millis() + timeout
        while self.millis() < timeout:
            buffer = self.__serialConnection.read(
                self.__serialConnection.inWaiting())

            if buffer:
                # convert the response to UTF-8
                response += (buffer.decode(encoding="utf8",
                                           errors='ignore'))
            # check if the command return code matches the code list expected
            for index in CommandResponse:
                if index.name in response:
                    stop = True
                    break

            if stop:
                break

        self.flush()

        return response # " ".join(response.split())


# DEBUG #
# this condition will only be True if the file is executed directly
if __name__ == "__main__":
    lorawan = SMW_SX1262M0("COM8")
    print(lorawan.ping())
