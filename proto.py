from sidh import genSecPubAlice, genSecPubBob
from sidh import MAX_Alice, MAX_Bob
from sidh import splits_Alice, splits_Bob
from sidh import shared_secret_Alice, shared_secret_Bob
from vernam import genVernamCipher

n_Alice, PKA = genSecPubAlice()
n_Bob, PKB = genSecPubBob()

SKA = shared_secret_Alice(n_Alice, PKB, splits_Alice, MAX_Alice)
print("Alice's shared secret:")
print(SKA)

SKB = shared_secret_Bob(n_Bob, PKA, splits_Bob, MAX_Bob)
print("Bob's shared secret:")
print(SKB)

if SKA == SKB:
        print('keys are equal :)')
else:
        print('something went wrong :(')
        if n_Alice % 2 != 0:
                print("Error: Alice's secret key must be even!")

SKA = str(SKA.re) + str(SKA.im)
SKB = str(SKB.re) + str(SKB.im)

def consume(msg, shared_secret):
    return genVernamCipher(msg, shared_secret), shared_secret[len(msg):]

msg = 'Hello world'
ciphered, SKA = consume(msg, SKA)
print('Ciphered text: %s' % ciphered)
ciphered, SKB = consume(ciphered, SKB)
print('Deciphered: %s' % ciphered)
assert msg == ciphered
assert SKA == SKB
print(len(SKA), len(SKB))
msg = 'Longer super secure random msg coming in.'
ciphered, SKA = consume(msg, SKA)
print('Ciphered text: %s' % ciphered)
ciphered, SKB = consume(ciphered, SKB)
print('Deciphered: %s' % ciphered)
assert msg == ciphered
assert SKA == SKB
print(len(SKA), len(SKB))
