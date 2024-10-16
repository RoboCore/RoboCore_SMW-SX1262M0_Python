RoboCore SMW-SX1262M0 Library (Python)
======================================

[![RoboCore LoRaWAN HAT - Helix Antenna](https://d229kd5ey79jzj.cloudfront.net/2568/images/2568_1_M.png)](https://www.robocore.net/hat-raspberry-pi/lorawan-hat-para-raspberry-pi)

 Python library for the [*RoboCore LoRaWAN HAT*](https://www.robocore.net/hat-raspberry-pi/lorawan-hat-para-raspberry-pi) using the SMW-SX1262M0 LoRaWAN transceiver.

Installation
------------

To install the library using [PIP](https://pip.pypa.io/en/stable/installation/), just use the command below.

`pip3 install RoboCore_SMW-SX1262M0`

> **Note:** this installation does not include examples.

Usage
-----

The LoRaWAN HAT uses GPIO 14 and 15 for communicating over the UART with the Raspberry Pi. This means that the UART port of the RPi must be previously enabled, and the serial console must be disabled.

Port to use on different models
* RPi 3 B+: `/dev/serial0` or `/dev/ttyS0`.
* RPi 4: `/dev/serial0` or `/dev/ttyS0`.
* RPi 5: `/dev/ttyAMA0`.
	** On the RPi 5, the serial console uses a dedicated UART.

Repository Contents
-------------------

* **/examples** - Examples of using the library (.py). Run them from an IDE that is compatible with Python.
* **/src** - Source files for the library (.py).
* **License.txt** - The license file of the library.

Documentation
-------------

* **[LoRaWAN Tutorials](https://www.robocore.net/tutoriais/internet-das-coisas/)** - Tutorials for using the LoRaWAN protocol.
* **[RoboCore LoRaWAN HAT - Helix Antenna](https://www.robocore.net/hat-raspberry-pi/lorawan-hat-para-raspberry-pi)** - Main webpage with technical data about the LoRaWAN HAT (Helix Antenna).
* **[GitHub](https://github.com/RoboCore/RoboCore_SMW-SX1262M0_Python)** - Project repository on GitHub.
* **[PyPI](https://pypi.org/user/RoboCore/)** - Project repository on PyPI.

Version History
---------------

* [v1.0.0](https://github.com/RoboCore/RoboCore_SMW-SX1262M0_Python) - First release.

License Information
-------------------

"SMW-SX1262M0-lib" is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"SMW-SX1262M0-lib" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with "SMW-SX1262M0-lib". If not, see <https://www.gnu.org/licenses/>
