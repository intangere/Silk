import msgpack
import string
import random

def build_userp(username):
    return msgpack.packb({'code' : '0', 'u' : username}, use_bin_type=True)

def build_msgp(to, _from, msg):
    return msgpack.packb({'code' : '1',  't' : to, 'f' : _from})

def username_takenp(username):
    return msgpack.packb({'code' : -1, 'u' : username}, use_bin_type=True)

def unpack(line):
    return msgpack.unpackb(line, raw=False)

def successp(_id):
    return msgpack.packb({'code' : '2', '_id' : _id}, use_bin_type=True)

def genID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

def offlinep(to):
    return msgpack.packb({'code' : '3', 't' : to}, user_bin_type=True)

def buildExchange(to, u, pub):
    return msgpack.packb({'code' : '4', 't' : to, 'p' : pub, 'u' : u}, use_bin_type=True)

def completeExchange(to, u, pub):
    return msgpack.packb({'code' : '5', 't' : to, 'p' : pub, 'u' : u}, use_bin_type=True)

def buildMessage(to, username, msg):
    return msgpack.packb({'code' : '6', 't' : to, 'u' : username, 'msg' : msg}, use_bin_type=True)

