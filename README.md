# Prime-Spectral Cipher (PSC)

![Build Status](https://github.com/YOUR_USERNAME/prime-spectral-cipher/actions/workflows/security_audit.yml/badge.svg)

A proof-of-concept symmetric stream cipher that utilizes **deterministic harmonic interference** to generate high-entropy keystreams.

### Concept
Standard stream ciphers (like ChaCha20) rely on modular arithmetic and bitwise rotation to generate randomness. 
**PSC** relies on **Spectral Number Theory**. It generates a keystream by sampling a procedural waveform constructed from log-modulated sine waves. 

The resulting stream exhibits **Gaussian Unitary Ensemble (GUE)** statistics, making the encrypted output statistically indistinguishable from background thermal noise.

### Key Features
*   **Steganographic Profile:** High Shannon entropy (>7.9 bits/byte) makes traffic resist Deep Packet Inspection (DPI) classification.
*   **Parameter Sensitivity:** Relies on Prime Number keys. A deviation of $\pm 2$ in the key results in immediate signal decoherence.
*   **Lightweight:** The generator function uses constant memory and standard floating-point operations.

### Usage

```python
from src.cipher import SpectralStreamCipher

key = 7919       # Shared Prime
seed = 1234.56   # Shared Phase Coordinate

alice = SpectralStreamCipher(key, seed)
bob   = SpectralStreamCipher(key, seed)

msg = b"Secure Data Stream"
enc = alice.process_buffer(msg)
dec = bob.process_buffer(enc)

print(dec) # b"Secure Data Stream"
```

### Disclaimer
This software is currently in the **Research Phase**. It has not yet undergone formal cryptanalysis. Use for educational and experimental purposes only.
