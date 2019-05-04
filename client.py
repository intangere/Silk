#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task, stdio
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from sidh import genSecPubAlice, genSecPubBob
from sidh import MAX_Alice, MAX_Bob
from sidh import splits_Alice, splits_Bob
from sidh import shared_secret_Alice, shared_secret_Bob
from sidh import Complex

from vernam import genVernamCipher
from protocol import *

import os

client = None

otpKeys = {}
msgQueue = {}

locked = False

def decodePubKey(data):

    pzero = data['p0'].split(',')
    pone = data['p1'].split(',')
    ptwo = data['p2'].split(',')

    return [ Complex(int(pzero[0]), int(pzero[1])),
             Complex(int(pone[0]), int(pone[1])),
             Complex(int(ptwo[0]), int(ptwo[1])) ]

class EchoClient(LineReceiver):

    def __init__(self):
        self.username = None
        self.mapper = {
                        '-1' : self.userTaken,
                        '3'  : self.userOffline,
                        '4'  : self.initExchange,
                        '5'  : self.sendMessage,
                        '6'  : self.readMessage
                      }

    def connectionMade(self):
        global client
        client = self
        print('Connected to Silk server')

    def lineReceived(self, line):
        data = unpack(line)
        self.mapper.get(data['code'], self.invalidPacket)(data)

    def userTaken(self, data):
        log('Username taken.')
        self.transport.loseConnection()

    def invalidPacket(self, data):
        print('Invalid packet with code %s' % data['code'])

    def userOffline(self, data):
        print('%s is offline. Cannot send message. Offline messaging is unsupported for now.' % data['t'])
        global locked
        locked = False

    def initExchange(self, data):
        """Receive the shared secret from the sender and finish the exchange
           SKB is bob's shared secret
        """
        n_Bob, PKB = genSecPubBob()
        Alice = decodePubKey(data)
        SKB = shared_secret_Bob(n_Bob, Alice, splits_Bob, MAX_Bob)
        otpKeys[data['u']] = SKB
        self.sendLine(completeExchange(data['u'], self.username, PKB))

    def sendMessage(self, data):
        shared = shared_secret_Alice(otpKeys[data['u']][0], decodePubKey(data), splits_Alice, MAX_Alice)
        shared = str(shared.re) + str(shared.im)
        self.sendLine(buildMessage(data['u'], data['t'], genVernamCipher(msgQueue[data['u']].pop(0), shared)))
        global locked
        locked = False

        otpKeys[data['u']] = os.urandom(1000)
        del otpKeys[data['u']]

    def readMessage(self, data):
        shared = str(otpKeys[data['u']].re) + str(otpKeys[data['u']].im)
        print('[%s]: %s' % (data['u'], genVernamCipher(data['msg'], shared)))
        global locked
        locked = False

        otpKeys[data['u']] = os.urandom(1000)
        del otpKeys[data['u']]

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

class ReadLine(LineReceiver):

    delimiter = b'\n' # unix terminal style newlines. remove this line
                      # for use with Telnet

    def __init__(self):
        self.locked = False

    def connectionMade(self):
        self.sendLine(b"Silk -000- Console. Type 'help' for help.")

    def lineReceived(self, line):
        if not line:
           return

        if locked:
           print('Key exchange taking place. Stdio locked.')
           return

        line = line.decode("ascii")
        cmd  = line.split(' ')[0]
        args = line.split(' ')[1:]

        try:
            handler = getattr(self, '_' + cmd)
            handler(args)
        except AttributeError as e:
            print(e)
            self.sendLine(b'Error: no such command.')

    def _name(self, args):
        if client:
           client.username = args[0]
           client.sendLine(build_userp(args[0]))
        else:
           print('You are not registered, cannot send.')

    def _send(self, args):

        if not client:
           print('Please wait till you\'re connected')
           return
        else:
          if not client.username:
             print('Select a username by typing \'name <your username>\'')
             return

        if args[0] == client.username:
           print('You may not send messages to yourself, yet.')
           return

        to = args[0]
        msg = ' '.join(args[1:])

        if len(msg) > 452:
           print('Message longer than 432 characters.')
           return

        n_Alice, PKA = genSecPubAlice()
        otpKeys[to] = (n_Alice, PKA)
        client.sendLine(buildExchange(to, client.username, PKA))

        global locked
        locked = True

        if to not in msgQueue.keys():
           msgQueue[to] = []

        msgQueue[to].append(msg)
        print('[%s]: %s' % (client.username, msg))

    def _quit(self, _):
        if client:
           client.transport.loseConnection()

    def _help(self, _):
        print("""
              help: Display this message
              name <username>: set username
              send <to> <msg>: send message
              quit: terminate connection and shutdown
              """)

    def __checkSuccess(self, pageData):
        msg = "Success: got {} bytes.".format(len(pageData))
        self.sendLine(msg.encode("ascii"))

    def connectionLost(self, reason):
        print('Stdio broke. Reactor stopping.')
        #reactor.stop()

def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    stdio.StandardIO(ReadLine())
    return factory.done

if __name__ == '__main__':
    task.react(main)
