# -*- coding: utf-8 *-*
import os
import time
import json
import random
import socket
import hashlib


class Client_Connection(object):

    def __init__(self, ip='bloocoin.zapto.org', port=3122, retry_timeout=10):
        """
            A client connection handles all client server operations.

            Keyword Arguments:
            ip -- The ip address of the server. Only provided to allow the
                    programatic changing of the server for debugging purposes.
            port -- The integer port to attempt to connect to the server on.
            retry_timeout -- The amount of time in seconds that the client
                    will wait before attempting to reconnect to the server.
        """
        self.ip = ip
        self.port = port
        self.retry_timeout = retry_timeout

    def has_bloostamp(self):
        """Checks if a bloostamp exists."""
        return os.path.exists('bloostamp')

    def get_commands(self):
        """Retrieves the names of all command functions."""
        return [cmd for cmd in dir(self) if 'cmd' in cmd]

    def read_file(self, filename, access='rb'):
        """
            Reads a the contents of a file.

            Arguments:
            filename -- The full path to the file to be read.

            Keywork arguments:
            access -- The file access flag.
        """
        contents = None
        with open(filename, access) as f:
            contents = f.readlines()
        return contents[0] if len(contents) is 1 else contents

    def write_file(self, filename, contents, access='w'):
        """
            Writes data to a file.

            Arguments:
            filename -- The full path to the file to be modified.
            contents -- The contents to be written to the file.

            Keyword arguments:
            access -- The file access flag.
        """
        contents = list(contents) if type(contents) in (tuple, list) \
                   else [contents, ]
        with open(filename, access) as f:
            f.writelines(contents)

    def get_addr(self):
        """Retrieves the BlooCoin address from the bloostamp."""
        return self.read_file('bloostamp').split(':')[0]

    def get_pwd(self):
        """Retrieves the BlooCoin key from the bloostamp."""
        return self.read_file('bloostamp').split(':')[1]

    def send_request(self, commands, multi_replies=False, ret_buf_size=1024):
        """
            Performs socket operations.

            Arguments:
            commands -- a dict containing json commands and parameters.

            Keyword arguments:
            multi_replies -- This flag allows the storage of multiple pieces of
                            data in a list. Defaults to False.
            ret_buf_size -- The size of the buffer when attempting to recv
                            data from the server. Defaults to 1024.
        """
        s = socket.socket()
        s.settimeout(3)
        data = [] if multi_replies else None
        while True:
            try:
                s.connect((self.ip, self.port))
                s.send(json.dumps(commands))
                if multi_replies:
                    while True:
                        temp = s.recv(ret_buf_size)
                        if temp is None or len(temp) is 0:
                            break
                        data.append(temp)
                else:
                    data = s.recv(ret_buf_size)
                break
            except socket.timeout:
                print 'Server seems to be down.. ' \
                      'Retrying in {0} seconds.'.format(self.retry_timeout)
                time.sleep(self.rety_timeout)
        s.close()
        return data

    def register(self):
        """Attempts to register a new address with the server."""
        stamp, addr, key, data = None, None, None, None
        while data != "True":
            stamp = self.generate_bloostamp()
            addr, key = stamp.split(':')
            commands = {'cmd': 'register',
                        'addr': addr,
                        'pwd': key}
            data = self.send_request(commands)
        data = ':'.join([stamp, '1'])
        self.write_file('bloostamp', data)

    def cmd_transactions(self):
        """Returns a list containing all transactions for this account."""
        commands = {'cmd': 'transactions',
                    'addr': self.get_addr(),
                    'pwd': self.get_pwd()}
        return self.send_request(commands, True)

    def cmd_coins(self):
        """Returns the amount of keys owned by this account."""
        commands = {'cmd': 'my_coins',
                    'addr': self.get_addr(),
                    'pwd': self.get_pwd()}
        return self.send_request(commands)

    def cmd_sendcoin(self, amount, to):
        """
            Sends coins to another BlooCoin account.

            Arguments:
            amount -- the amount of BlooCoins to send.
            to -- the address of the recipient.
        """
        commands = {'cmd': 'send_coin',
                    'amount': amount,
                    'to': to,
                    'addr': self.get_addr(),
                    'pwd': self.get_pwd()}
        return self.send_request(commands)

    def update(self):
        """Checks for core updates.
            Returns a string description of the recieved data."""
        commands = {'ver': self.ver,
                    'cmd': 'update',
                    'type': self.type}
        res = {
            '0': 'Your client is running the latest version!\n',
            '1': 'A new version is available.'
                 'It can be downloaded at\:n'
                 'AddressHere\n',
            '2': '\n'}
        data = self.send_request(commands)
        return 'Server seems to be offline!' if data is None else res[data[0]]

    def generate_bloostamp(self):
        """Generates a new bloostamp"""
        import string
        chars = string.letters + string.digits
        # Generate address
        addr = ''.join([random.choice(chars) for i in xrange(100)])
        for i in xrange(50):
            addr = hashlib.sha1(addr).hexdigest()
        # Generate key
        key = ''.join([random.choice(chars) for i in xrange(5000)])
        for i in xrange(1000):
            key = hashlib.sha1(key).hexdigest()
        return ':'.join([addr, key])
