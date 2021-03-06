def genVernamCipher( text, key ):
    """ Returns the Vernam Cipher for given string and key """
    answer = "" # the Cipher text
    p = 0 # pointer for the key
    for char in text:
        answer += chr(ord(char) ^ ord(key[p]))
        p += 1
        if p==len(key):
            p = 0
    return answer
