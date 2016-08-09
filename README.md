# knuckleball-py
Python client for [Knuckleball](https://github.com/ral99/knuckleball) data structure server.

## Installing
This client is being tested on Python 2 and Python 3. To install, type:
```
$ python setup.py install
```

## Getting started
First, instantiate `Knuckleball` with the server parameters. Then, send commands to the server with its method `execute`.
```
>> from knuckleball.client import Knuckleball
>> knuckleball = Knuckleball(host='127.0.0.1', port=8001, timeout_in_seconds=3.0)
>> knuckleball.execute('Set<String> create: players;')
>> knuckleball.execute('players add: "Babe Ruth";')
>> knuckleball.execute('players add: "David Ortiz";')
>> knuckleball.execute('players add: "Paulo Orlando";')
>> knuckleball.execute('players get;')
{'Babe Ruth', 'David Ortiz', 'Paulo Orlando'}
>> knuckleball.execute('players contains? "Mariano Rivera";')
False
```
