# -*- coding: utf-8 *-*
import cmd
import argparse
import core
import util


class Console(cmd.Cmd):

    __slots__ = ['client', 'debug', 'prompt', 'intro']

    def __init__(self, args):
        cmd.Cmd.__init__(self)
        self.intro = 'Welcome to BlooClient-cli.\n' \
                     'Type help or ? for a list of commands.\n'
        self.debug = args.debug
        self.client = core.Client_Connection(args.ip, args.port, args.timeout)
        if not self.debug:
            if util.update(self.__module__):
                print 'Client has been updated. Please restart!\n'
            if self.client.update():
                print 'The core module has been updated! Please restart!\n'
            if util.update(util.__name__):
                print 'The util module has been updated! Please restart!\n'
        self.prompt = 'BlooClient: '
        if not self.client.has_bloostamp():
            print 'No bloostamp found, creating one!'
            self.client.register()
            self.do_addr('')

    def do_addr(self, line):
        """
            Syntax: addr
            Returns the bloocoin address.
        """
        if len(line) > 0:
            print 'Invalid arguments!\n'
            return
        print 'Your bloocoin address is', self.client.get_addr(), '\n'

    def do_transactions(self, line):
        """
            Syntax: transactions
            Retrieves all known transactions for the current account.
        """
        if len(line) > 0:
            print 'Invalid arguments!\n'
            return
        transactions = self.client.cmd_transactions()
        if len(transactions) is not 0:
            for transaction in transactions:
                print transaction
        else:
            print 'No transactions for this account exist.\n'

    def do_coins(self, line):
        """
            Syntax: coins
            Retrieves the amount of coins owned by this account.
        """
        if len(line) > 0:
            print 'Invalid arguments!'
            return
        print 'You currently have {0} coins.\n'.format(
            self.client.cmd_coins())

    def do_sendcoin(self, line):
        """
            Syntax: sendcoin <amount> <recipient>
            Sends coins to another account.

            Arguments:
                amount: How many coins to send.
                recipient: The address of the recipient.
        """
        types = [int, str]
        args = self.parse(line, types)
        if len(args) > 3 or not self.right_types(args, types):
            print 'Invalid arguments!\n'
            return
        print self.client.cmd_sendcoin(args[0], args[1])

    def parse(self, args, types):
        """Parses arguments and attempts to convert them to required types."""
        args = args.split(' ')
        for i in xrange(len(types)):
            temp = args[i]
            try:
                args[i] = types[i](temp)
            except:
                args[i] = temp
        return args

    def right_types(self, args, types):
        """Check if the contens of args have the right types."""
        for i in xrange(len(types) - 1):
            if not isinstance(args[i], types[i]):
                return False
        return True

    def do_quit(self, line):
        """
            Syntax: quit
            Closes the client.
        """
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enables debug mode... Dahhh!')
    parser.add_argument('-i', '--ip', type=str, default='server.bloocoin.org',
                        help='The BlooCoin server ip address.')
    parser.add_argument('-p', '--port', type=int, default=3122,
                        help='The port to connect to on the BlooCoin server.')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Time in second to wait between attempting '
                             'server connections.')
    args = parser.parse_args()
    c = Console(args)
    c.cmdloop()
