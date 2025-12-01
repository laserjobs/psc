import unittest
import math
from collections import Counter
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cipher import SpectralStreamCipher

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    total = len(data)
    counts = Counter(data)
    
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

class TestSpectralCipher(unittest.TestCase):

    def setUp(self):
        self.prime_key = 7919
        self.seed = 98765.4321
        self.payload = b"This is a test of the Spectral Noise encryption protocol. " * 100

    def test_integrity(self):
        """Ensure Dec(Enc(M)) == M"""
        alice = SpectralStreamCipher(self.prime_key, self.seed)
        bob = SpectralStreamCipher(self.prime_key, self.seed)
        
        encrypted = alice.process_buffer(self.payload)
        decrypted = bob.process_buffer(encrypted)
        
        self.assertEqual(self.payload, decrypted, "Decryption failed to recover original text.")

    def test_key_sensitivity(self):
        """Ensure a slightly wrong key produces garbage (Avalanche Effect)"""
        alice = SpectralStreamCipher(self.prime_key, self.seed)
        # Eve is off by 2 integers on the prime key
        eve = SpectralStreamCipher(self.prime_key - 2, self.seed)
        
        encrypted = alice.process_buffer(self.payload)
        eve_attempt = eve.process_buffer(encrypted)
        
        self.assertNotEqual(self.payload, eve_attempt, "Wrong key successfully decrypted message (Security Failure).")

    def test_entropy(self):
        """Ensure ciphertext is statistically indistinguishable from noise"""
        alice = SpectralStreamCipher(self.prime_key, self.seed)
        encrypted = alice.process_buffer(self.payload)
        
        ent = calculate_entropy(encrypted)
        print(f"\n[METRICS] Shannon Entropy: {ent:.4f} bits/byte (Ideal: 8.0)")
        
        # We expect high entropy (> 7.5 for this short sample)
        self.assertGreater(ent, 7.5, "Entropy is too low; pattern is detectable.")

if __name__ == '__main__':
    unittest.main()
