# Silk
SIDH Ephemeral Messaging Protocol
<hr>
This entire repository is containing the initial raw code.
Do NOT ask me questions how to to use it nor do I recommend you use it yet, ONLY if it's in private.
Right now only 452 character messages are supported.
Run 
`
server.py
`
to start the server.
Run client.py to connect.
After connecting type
`
name <the username you want>
`
To send a message type
`
send <to username> <your message here>
This library uses a SIDH key exchange with a vernam cipher after the exchange.
There is no point in using AES after the exchange. 
If SIDH ends up being broken, and your AES key is based off the exchange.. it's pointless.
<br>
Each message uses a new SIDH key which should be self explanatory.
<br>
I'll rewrite this description and document it once the library is actually ready for use.

