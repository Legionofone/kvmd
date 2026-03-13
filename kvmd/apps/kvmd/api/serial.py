# ========================================================================== #
#                                                                            #
#    KVMD - The main PiKVM daemon.                                           #
#                                                                            #
#    Copyright (C) 2018-2021  Maxim Devaev <mdevaev@gmail.com>               #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                            #
# ========================================================================== #

import serial

from aiohttp.web import Request
from aiohttp.web import Response

from ....htserver import exposed_http
from ....htserver import make_json_response

# Baud rate of serial adapter
serial_baudrate = 9600
# COM port or device for serial adapter
serial_port = '/dev/ttyUSB0'
# Serial command KVM uses to switch ports
kvm_port_command = '0xAA 0xBB 0x03 0x01 0x{port}0xEE\r\n'

# =====
class SerialApi:
    def __init__(self) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = '/dev/ttyUSB0'

    # ===== SERIAL STUFF

    @exposed_http("GET", "/serial")
    async def __serial_command(self, request):
        port = request.query.get('port')
        kvm_port = kvm_port_command.format(**{'port': port})
        change_string = bytearray([0xAA, 0xBB, 0x03, 0x01, int(str(port).zfill(2)), 0xEE])
        with self.ser:
            self.ser.write(change_string)
        return make_json_response({"port": port})
