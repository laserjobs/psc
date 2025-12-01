import sys
import os
import binascii

# Import the Cipher from the source folder
sys.path.insert(0, os.path.abspath('src'))
from cipher import SpectralStreamCipher

def print_hex_dump(label, data, limit=32):
    """Pretty prints binary data in Hex format"""
    hex_str = binascii.hexlify(data).decode('utf-8').upper()
    truncated = ""
    if len(hex_str) > limit*2:
        truncated = "..."
    print(f"{label:<15}: {hex_str[:limit*2]}{truncated} ({len(data)} bytes)")

def run_demo():
    print("="*60)
    print("   PRIME-SPECTRAL CIPHER (PSC) - VISUAL DEMONSTRATION")
    print("="*60)

    # 1. SETUP
    PRIME_KEY = 7919
    SEED = 12345.6789
    MESSAGE = b"The quick brown fox jumps over the lazy dog."
    
    print(f"\n[CONFIGURATION]")
    print(f"Key (Prime):     {PRIME_KEY}")
    print(f"Seed (Phase):    {SEED}")
    print(f"Plaintext:       '{MESSAGE.decode('utf-8')}'")

    # 2. ENCRYPTION (ALICE)
    print("\n[STEP 1: ENCRYPTION]")
    alice = SpectralStreamCipher(PRIME_KEY, SEED)
    encrypted = alice.process_buffer(MESSAGE)
    print_hex_dump("Ciphertext", encrypted)

    # 3. DECRYPTION (BOB - CORRECT KEY)
    print("\n[STEP 2: DECRYPTION (Valid Key)]")
    bob = SpectralStreamCipher(PRIME_KEY, SEED)
    decrypted = bob.process_buffer(encrypted)
    print(f"Recovered:       '{decrypted.decode('utf-8')}'")
    
    if decrypted == MESSAGE:
        print("Status:          SUCCESS (Match)")
    else:
        print("Status:          FAILURE (Mismatch)")

    # 4. ATTACK SIMULATION (EVE - WRONG KEY)
    print("\n[STEP 3: ATTACK SIMULATION (Wrong Key)]")
    # Eve guesses a prime that is extremely close (Twin Prime scenario)
    WRONG_KEY = 7907 
    print(f"Attacker Key:    {WRONG_KEY} (Delta: {abs(PRIME_KEY - WRONG_KEY)})")
    
    eve = SpectralStreamCipher(WRONG_KEY, SEED)
    eve_attempt = eve.process_buffer(encrypted)
    
    print_hex_dump("Eve Result", eve_attempt)
    try:
        print(f"Eve Decoded:     '{eve_attempt.decode('utf-8')}'")
    except UnicodeDecodeError:
        print(f"Eve Decoded:     (Binary Garbage - Not valid UTF-8)")

    # 5. VISUALIZING THE KEYSTREAM
    # We will generate just the noise to show what the "Zeta Stream" looks like
    print("\n[STEP 4: KEYSTREAM VISUALIZATION]")
    print("Generating raw spectral noise (first 16 bytes)...")
    temp_cipher = SpectralStreamCipher(PRIME_KEY, SEED)
    dummy_input = b'\x00' * 16 # XORing with 0 reveals the keystream
    keystream = temp_cipher.process_buffer(dummy_input)
    print_hex_dump("Keystream", keystream)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_demo()
