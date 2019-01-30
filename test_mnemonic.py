#!/usr/bin/env python

import pprint
import string
from random import SystemRandom, randrange
from binascii import hexlify, unhexlify
from moneywagon import generate_keypair
from mnemonic import mnemonic

pp = pprint.PrettyPrinter(indent=2)

def gen_rand():
    foo = SystemRandom()
    length = 32
    chars = string.hexdigits
    return ''.join(foo.choice(chars) for _ in range(length))

mnemo = mnemonic.Mnemonic('english')

entropy = gen_rand()
entropy = '00000000000000000000000000000000'

words = mnemo.to_mnemonic(unhexlify(entropy))
seed = hexlify(mnemo.to_seed(words))
address = generate_keypair('btc', '1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67')

print(words)
print(seed)
pp.pprint(address)
#print(address['public']['address'])
#print(address['private']['hex'])