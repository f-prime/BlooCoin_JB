# -*- coding: utf-8 *-*
import cmd
import core


class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.client = core.Client_Connection()
        self.prompt = 'BlooClient: '
        if not self.client.has_bloostamp():
            print 'No bloostamp found, creating one!'
            self.client.register()
        self.do_addr('')

    def do_addr(self, line):
        """Returns the bloocoin address."""
        if len(line) > 0:
            print "Invalid arguments!"
            return
        print "Your bloocoin address is", self.client.get_addr()

    def do_transactions(self, line):
        """Retrieves all known transactions for the current account."""
        if len(line) > 0:
            print "Invalid arguments!"
            return
        transactions = self.client.cmd_transactions()
        if len(transactions) is not 0:
            for transaction in transactions:
                print transaction
        else:
            print 'No transactions for this account exist.'

    def do_coins(self, line):
        """Retrieves the amount of coins owned by this account."""
        if len(line) > 0:
            print "Invalid arguments!"
            return
        print 'You currently have {0} coins.'.format(
            self.client.cmd_coins())

    def do_sendcoin(self, line):
        """
            Sends coins to another account.

            Arguments:
                amount: How many coins to send.
                recipient: The address of the recipient.
        """
        types = [int, str]
        args = self.parse(line, types)
        if len(args) > 3 or not self.right_types(args, types):
            print "Invalid arguments!"
            return
        ret = self.client.cmd_sendcoin(args[0], args[1])
        print ret

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
        """Closes the client."""
        return True

if __name__ == '__main__':
    c = Console()
    c.cmdloop()
