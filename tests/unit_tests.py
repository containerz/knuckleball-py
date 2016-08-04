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

# Add source code directory to path
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'src'))

import unittest

from knuckleball.client import Knuckleball
from knuckleball.exception import KnuckleballException

class KnuckleballTest(unittest.TestCase):
    def test_parse(self):
        # null
        self.assertEqual(Knuckleball.parse('null'), None)

        # Boolean
        self.assertEqual(Knuckleball.parse('true'), True)
        self.assertEqual(Knuckleball.parse('false'), False)

        # Character
        self.assertEqual(Knuckleball.parse("'a'"), 'a')
        self.assertEqual(Knuckleball.parse("'z'"), 'z')
        self.assertEqual(Knuckleball.parse("'A'"), 'A')
        self.assertEqual(Knuckleball.parse("'Z'"), 'Z')
        self.assertEqual(Knuckleball.parse("'0'"), '0')
        self.assertEqual(Knuckleball.parse("'9'"), '9')

        # Integer
        self.assertEqual(Knuckleball.parse('0'), 0)
        self.assertEqual(Knuckleball.parse('9'), 9)
        self.assertEqual(Knuckleball.parse('-9'), -9)
        self.assertEqual(Knuckleball.parse('99'), 99)

        # Float
        self.assertEqual(Knuckleball.parse('0.000'), 0.000)
        self.assertEqual(Knuckleball.parse('0.001'), 0.001)
        self.assertEqual(Knuckleball.parse('-0.01'), -0.01)
        self.assertEqual(Knuckleball.parse('10.99'), 10.99)
        self.assertEqual(Knuckleball.parse('-9.00'), -9.00)

        # String
        self.assertEqual(Knuckleball.parse('""'), '')
        self.assertEqual(Knuckleball.parse('"knuckleball"'), 'knuckleball')
        self.assertEqual(Knuckleball.parse('"knuckle ball"'), 'knuckle ball')
        self.assertEqual(Knuckleball.parse('"knuckle\\"ball"'), 'knuckle"ball')

        # Vector
        self.assertEqual(Knuckleball.parse('[]'), [])
        self.assertEqual(Knuckleball.parse('[true,false]'), [True, False])
        self.assertEqual(Knuckleball.parse("['0']"), ['0'])
        self.assertEqual(Knuckleball.parse('[-42,0,42]'), [-42, 0, 42])
        self.assertEqual(Knuckleball.parse('[-42.00,0.00,42.00]'), [-42.00, 0.00, 42.00])
        self.assertEqual(Knuckleball.parse('["knuckle","","ball"]'), ["knuckle", "", "ball"])
        self.assertEqual(Knuckleball.parse('[i,prices,std::ages]'), ['i', 'prices', 'std::ages'])

        # Set
        self.assertEqual(Knuckleball.parse('{}'), set([]))
        self.assertEqual(Knuckleball.parse('{true,false}'), set([True, False]))
        self.assertEqual(Knuckleball.parse("{'0'}"), set(['0']))
        self.assertEqual(Knuckleball.parse('{-42,0,42}'), set([-42, 0, 42]))
        self.assertEqual(Knuckleball.parse('{-42.00,0.00,42.00}'), set([-42.00, 0.00, 42.00]))
        self.assertEqual(Knuckleball.parse('{"knuckle","","ball"}'), set(["knuckle", "", "ball"]))

        # Dictionary
        self.assertEqual(Knuckleball.parse('()'), {})
        self.assertEqual(Knuckleball.parse('(("knuckle",false),("ball",true))'), {'knuckle': False, 'ball': True})
        self.assertEqual(Knuckleball.parse("(('a',42))"), {'a': 42})
        self.assertEqual(Knuckleball.parse('((42,"knuckle"),(-42,"ball"))'), {42: 'knuckle', -42: 'ball'})
        self.assertEqual(Knuckleball.parse('(("a",-42.0),("b",42.0),("c",0.0))'), {'a': -42.0, 'b': 42.0, 'c': 0.0})

        # Exceptions
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'SyntaxError: invalid statement.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: invalid argument.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: invalid message.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: variable name already used.')
        self.assertRaises(KnuckleballException, Knuckleball.parse,
                          'RuntimeError: name cannot be resolved to a variable.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: wrong number of arguments.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: cannot compare these two types.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'AuthenticationError: not authenticated.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'AuthenticationError: wrong password.')
        self.assertRaises(KnuckleballException, Knuckleball.parse, 'RuntimeError: unknown error.')

    def test_execute(self):
        knuckleball = Knuckleball(8001, password='securepassword')

        # Boolean
        self.assertEqual(knuckleball.execute('Boolean create: t withValue: true;'), None)
        self.assertEqual(knuckleball.execute('t get;'), True)

        # Character
        self.assertEqual(knuckleball.execute("Character create: numeric withValue: '9';"), None)
        self.assertEqual(knuckleball.execute('numeric get;'), '9')

        # Integer
        self.assertEqual(knuckleball.execute('Integer create: i withValue: 42;'), None)
        self.assertEqual(knuckleball.execute('i get;'), 42)

        # Float
        self.assertEqual(knuckleball.execute('Float create: f withValue: 1e-2;'), None)
        self.assertEqual(knuckleball.execute('f get;'), 0.010)

        # String
        self.assertEqual(knuckleball.execute('String create: str withValue: "knuckleball";'), None)
        self.assertEqual(knuckleball.execute('str get;'), 'knuckleball')

        # Vector
        self.assertEqual(knuckleball.execute('Vector<Integer> create: prices;'), None)
        self.assertEqual(knuckleball.execute('prices get;'), [])

        # Set
        self.assertEqual(knuckleball.execute('Set<String> create: ids;'), None)
        self.assertEqual(knuckleball.execute('ids get;'), set([]))

        # Dictionary
        self.assertEqual(knuckleball.execute('Dictionary<String, Integer> create: std::ages;'), None)
        self.assertEqual(knuckleball.execute('std::ages get;'), {})

        # Context
        self.assertEqual(knuckleball.execute('Context listVariables;'),
                         ['f', 'i', 'ids', 'numeric', 'prices', 'std::ages', 'str', 't'])
        self.assertEqual(knuckleball.execute('Context listNamespaces;'), ['std'])

        # unauthenticated request
        knuckleball = Knuckleball(8001)
        self.assertRaises(KnuckleballException, knuckleball.execute, 'i get;')

        # wrong password
        self.assertRaises(KnuckleballException, Knuckleball, 8001, password='wrongpassword')

if __name__ == '__main__':
    unittest.main()
