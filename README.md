# Silk (ALPHA)
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
<b>Edit: I've now found reason to support AES keys. "Longer messages"</b></br>
<br>
That being said I'd probably split the exchanged key and pad+cipher the text itself.<br>
<br>
<br>
Each message uses a new SIDH key which should be self explanatory.<br>
I'll rewrite this description and document it once the library is actually ready for use.<br>

<h1>Todo</h1>
<br>
<pre>
  - Make messaging yourself possible
  - Username registration rather than one time names
  - Offline messaging via a mailbox type structure
  - ./silk -read (read missed messages without staying online)
  - ./silk -send <to> <msg> (write messages without staying online)
  - ./silk -shred
  - Contact storage
  - User fingerprints for user verification 
  - bug where username isn't properly freed
  - [DONE]: Delete shared secrets immediately after use
  - [DONE]: Remove the only usage of eval
  - [DONE]: Write actual event handlers instead of bootleg if statements
</pre>
<h3>Ideas</h3>
<pre>
  - Time-frame locked messages which have to be opened within x amount of seconds
    or the receiever can no longer read the messages. Both users have to be online
    for something like this to work.
  - SPHINCS(+)-256 Signatures for identity verification
  - Use the one time exhanged key to seed a mersenee twister based on the key if the
    key isn't long enough to vernam cipher the text. Use that then to cipher the text. Probably pad the text too.
  - Perhaps cipher the text with a seed attached randomly in the message before it's vernam ciphered and padded. 
</pre>
