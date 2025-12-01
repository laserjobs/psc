import math
import struct

class SpectralStreamCipher:
    def __init__(self, sampling_key: int, phase_seed: float):
        """
        Initializes the stream generator.
        
        Args:
            sampling_key (int): A prime number representing the sampling stride.
            phase_seed (float): The initial coordinate on the harmonic function.
        """
        self.p = float(sampling_key)
        self.t = float(phase_seed)
        
    def _generate_noise_byte(self) -> int:
        """
        Generates a deterministic chaotic byte using harmonic interference.
        
        Mechanism:
        Summation of sine waves modulated by the logarithm of harmonic indices.
        This creates a non-repeating, high-entropy signal (Spectral Noise).
        """
        val = 0.0
        # Summation of the first 5 log-modulated harmonics
        for k in range(1, 6):
            val += math.sin(self.t * self.p * math.log(k + 1))
        
        # Advance the phase coordinate (step size avoids immediate harmonic locks)
        self.t += 0.1337 
        
        # Scaling and quantization to 8-bit integer
        scaled = (val + 100.0) * 10000.0
        return int(scaled) % 256

    def process_buffer(self, data: bytes) -> bytes:
        """
        Applies the keystream to the input buffer via XOR.
        Used for both Encryption and Decryption (Symmetric).
        """
        output = bytearray()
        for byte in data:
            keystream_byte = self._generate_noise_byte()
            output.append(byte ^ keystream_byte)
        return bytes(output)
