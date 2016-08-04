# Copyright (c) 2016, Rodrigo Alves Lima
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#        following disclaimer.
# 
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#        following disclaimer in the documentation and/or other materials provided with the distribution.
# 
#     3. Neither the name of knuckleball-py nor the names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import sys

class TCPConnection:
    def __init__(self, host, port, timeout_in_seconds=None):
        "Set a TCP connection with the server or raise an error."
        self._sock = None
        self._buffer = ''
        for addrinfo in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            try:
                self._connect(timeout_in_seconds, *addrinfo)
            except:
                if self._sock is not None:
                    self._sock.close()
                    self._sock = None
            if self._sock is not None:
                break
        if self._sock is None:
            raise socket.error('unable to connect.')

    def __del__(self):
        "Close the socket, if it exists."
        try:
            self._sock.close()
        except:
            pass

    def _connect(self, timeout_in_seconds, family, socktype, proto, canonname, sockaddr):
        "Try to connect to the server using the specified parameters."
        self._sock = socket.socket(family, socktype, proto)
        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._sock.settimeout(timeout_in_seconds);
        self._sock.connect(sockaddr)

    def send(self, data):
        "Send all data to the socket."
        if sys.version_info >= (3, 0):
            self._sock.sendall(bytes(data, 'utf8'))
        else:
            self._sock.sendall(bytes(data))

    def recv(self):
        "Receive data from the socket and return it until '\n'."
        while self._buffer.find('\n') < 0:
            received = self._sock.recv(4096)
            if len(received) == 0:
                raise socket.error('connection closed by foreign host.')
            self._buffer += received.decode('utf8')
        data = self._buffer[:self._buffer.find('\n')]
        self._buffer = self._buffer[len(data) + 1:]
        return data
