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

