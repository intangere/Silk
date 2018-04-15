#!/usr/bin/env python
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import msgpack
from protocol import *

### Protocol Implementation

def log(msg):
    print('[INFO]: %s' % msg)


users = {}
class Echo(Protocol):

    def __init__(self):
        self.username = None

    def dataReceived(self, data):

        pdata = data
        data = msgpack.unpackb(data[:-2], raw=False)

        if data['code'] == '0':
           if data['u'] not in users.keys():
              self.username = data['u']
              users[self.username] = self
              log('%s connected successfully' % self.username)
           else:
              log('Username %s taken' % data['u'])
              self.sendLine(username_takenp(username))
              self.transport.close() #send username taken

        if data['code'] == '4' or data['code'] == '5' or data['code'] == '6':
           if data['u'] in users.keys():
              if data['t'] in users.keys():
                 users[data['t']].transport.write(pdata)
              else:
                 self.sendLine(offlinep(data['t']))

    def connectionLost(self, reason):
        if self.username:
           del users[self.username]
           print('%s disconnected' % self.username)
        else:
           print('Failed connection')

def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()

