# Silk (NOT READY)
SIDH Ephemeral Messaging Protocol
<hr>
This entire repository is containing the initial raw code.<br>
Do NOT ask me questions how to to use it nor do I recommend you use it yet, ONLY if it's in private.<br>
Right now only 452 character messages are supported.<br>
Run <br>

```
server.py
```

to start the server.
Run client.py to connect.
After connecting type

```
name <the username you want>
```

To send a message type

```
send <to username> <your message here>
```

This library uses a SIDH key exchange with a vernam cipher after the exchange.<br>
There is no point in using AES after the exchange. <br>
If SIDH ends up being broken, and your AES key is based off the exchange.. it's pointless.<br>
<br>
Each message uses a new SIDH key which should be self explanatory.<br>
<br>
I'll rewrite this description and document it once the library is actually ready for use.<br>

