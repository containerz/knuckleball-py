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

from knuckleball import connection
from knuckleball import exception

class Knuckleball:
    def __init__(self, host, port, timeout_in_seconds=None, password=None):
        "Set a TCP connection with the Knuckleball server or raise an error."
        self._tcp_connection = connection.TCPConnection(host, port, timeout_in_seconds)
        if password:
            self.execute('Connection authenticate: "%s";' % password)

    def execute(self, command):
        "Execute a command in the Knuckleball server and return the result or raise an error."
        self._tcp_connection.send(command + "\n")
        data = self._tcp_connection.recv()
        return Knuckleball.parse(data)

    @staticmethod
    def parse(data):
        if Knuckleball._is_null(data):
            return None
        if Knuckleball._is_boolean(data):
            return Knuckleball._parse_boolean(data)
        if Knuckleball._is_character(data):
            return Knuckleball._parse_character(data)
        if Knuckleball._is_integer(data):
            return Knuckleball._parse_integer(data)
        if Knuckleball._is_float(data):
            return Knuckleball._parse_float(data)
        if Knuckleball._is_string(data):
            return Knuckleball._parse_string(data)
        if Knuckleball._is_vector(data):
            return Knuckleball._parse_vector(data)
        if Knuckleball._is_set(data):
            return Knuckleball._parse_set(data)
        if Knuckleball._is_dictionary(data):
            return Knuckleball._parse_dictionary(data)
        if Knuckleball._is_error(data):
            raise exception.KnuckleballException(data)
        raise exception.KnuckleballException('invalid value.')

    @staticmethod
    def _is_null(data):
        return data == "null"

    @staticmethod
    def _is_error(data):
        return data.startswith('SyntaxError:') or data.startswith('RuntimeError:') or \
               data.startswith('AuthenticationError:')

    @staticmethod
    def _is_boolean(data):
        return data in ('true', 'false')

    @staticmethod
    def _parse_boolean(data):
        return data == 'true'

    @staticmethod
    def _is_character(data):
        return len(data) == 3 and data[0] == "'" and data[2] == "'"

    @staticmethod
    def _parse_character(data):
        return data[1]

    @staticmethod
    def _is_integer(data):
        return data.isdigit() or (len(data) > 1 and data[0] in ('+', '-') and data[1:].isdigit())

    @staticmethod
    def _parse_integer(data):
        return int(data)

    @staticmethod
    def _is_float(data):
        return Knuckleball._is_integer(data) or (data.find('.') >= 0 and
               Knuckleball._is_integer(data[:data.find('.')]) and Knuckleball._is_integer(data[data.find('.') + 1:]))

    @staticmethod
    def _parse_float(data):
        return float(data)

    @staticmethod
    def _is_string(data):
        if len(data) > 1 and data[0] == '"' and data[-1] == '"':
            for i in range(1, len(data) - 1):
                if data[i] == '"':
                    for j in range(i - 1, -1, -1):
                        if data[j] != '\\':
                            if (i - j) % 2 == 1:
                                return False
                            break
            for i in range(len(data) - 2, 0, -1):
                if data[i] != '\\':
                    return (len(data) - 1 - i) % 2 == 1
            return len(data) % 2 == 0
        return False
            
    @staticmethod
    def _parse_string(data):
        data = data[1:-1]
        value = ""
        for i in range(len(data)):
            if i < len(data) - 1 and data[i] == '\\' and data[i + 1] == '"':
                continue
            value += data[i]
        return value

    @staticmethod
    def _is_identifier(data):
        if len(data) == 0 or not data[0].isalpha():
            return False
        for c in data[1:]:
            if not c.isalpha() and not c.isdigit() and c != '_':
                return False
        return True

    @staticmethod
    def _is_namespace(data):
        return Knuckleball._is_identifier(data)

    @staticmethod
    def _is_variable(data):
        for i in range(len(data) - 1):
            if data[i] == ':' and data[i + 1] == ':':
                return Knuckleball._is_namespace(data[:i]) and Knuckleball._is_identifier(data[i + 2:])
        return Knuckleball._is_identifier(data)

    @staticmethod
    def _is_value(data):
        return Knuckleball._is_boolean(data) or Knuckleball._is_character(data) or Knuckleball._is_integer(data) or \
               Knuckleball._is_float(data) or Knuckleball._is_string(data) or Knuckleball._is_namespace(data) or \
               Knuckleball._is_variable(data)

    @staticmethod
    def _parse_value(data):
        if Knuckleball._is_boolean(data):
            return Knuckleball._parse_boolean(data)
        if Knuckleball._is_character(data):
            return Knuckleball._parse_character(data)
        if Knuckleball._is_integer(data):
            return Knuckleball._parse_integer(data)
        if Knuckleball._is_float(data):
            return Knuckleball._parse_float(data)
        if Knuckleball._is_string(data):
            return Knuckleball._parse_string(data)
        if Knuckleball._is_namespace(data) or Knuckleball._is_variable(data):
            return data

    @staticmethod
    def _is_comma_separated_values(data):
        for i in range(len(data)):
            if data[i] == ',' and Knuckleball._is_value(data[:i]) and \
               Knuckleball._is_comma_separated_values(data[i + 1:]):
                return True
        return not data or Knuckleball._is_value(data)

    @staticmethod
    def _parse_comma_separated_values(data):
        values = []
        while data:
            for i in range(len(data)):
                if data[i] == ',' and Knuckleball._is_value(data[:i]):
                    values.append(Knuckleball._parse_value(data[:i]))
                    data = data[i + 1:]
                    break
            else:
                values.append(Knuckleball._parse_value(data))
                data = ''
        return values

    @staticmethod
    def _is_tuple(data):
        return len(data) > 1 and data[0] == '(' and data[-1] == ')' and \
               Knuckleball._is_comma_separated_values(data[1:-1]) and \
               len(Knuckleball._parse_comma_separated_values(data[1:-1])) == 2

    @staticmethod
    def _parse_tuple(data):
        return Knuckleball._parse_comma_separated_values(data[1:-1])

    @staticmethod
    def _is_comma_separated_tuples(data):
        for i in range(len(data)):
            if data[i] == ',' and Knuckleball._is_tuple(data[:i]) and \
               Knuckleball._is_comma_separated_tuples(data[i + 1:]):
                return True
        return not data or Knuckleball._is_tuple(data)

    @staticmethod
    def _parse_comma_separated_tuples(data):
        values = []
        while data:
            for i in range(len(data)):
                if data[i] == ',' and Knuckleball._is_tuple(data[:i]):
                    values.append(Knuckleball._parse_tuple(data[:i]))
                    data = data[i + 1:]
                    break
            else:
                values.append(Knuckleball._parse_tuple(data))
                data = ''
        return values

    @staticmethod
    def _is_vector(data):
        return len(data) > 1 and data[0] == '[' and data[-1] == ']' and \
               Knuckleball._is_comma_separated_values(data[1:-1])

    @staticmethod
    def _parse_vector(data):
        return Knuckleball._parse_comma_separated_values(data[1:-1])

    @staticmethod
    def _is_set(data):
        return len(data) > 1 and data[0] == '{' and data[-1] == '}' and \
               Knuckleball._is_comma_separated_values(data[1:-1])

    @staticmethod
    def _parse_set(data):
        return set(Knuckleball._parse_comma_separated_values(data[1:-1]))

    @staticmethod
    def _is_dictionary(data):
        return len(data) > 1 and data[0] == '(' and data[-1] == ')' and \
               Knuckleball._is_comma_separated_tuples(data[1:-1])

    @staticmethod
    def _parse_dictionary(data):
        return dict(Knuckleball._parse_comma_separated_tuples(data[1:-1]))
