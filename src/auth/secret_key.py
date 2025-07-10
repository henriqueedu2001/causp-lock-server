import secrets
import hashlib
from typing import *

class SecretKey:
    def __init__(self, key: bytes = None):
        self.value = SecretKey.cast_key_to_bytes(key) if key else SecretKey.generate_key()
    
    
    def cast_key_to_bytes(key: Union[bytes, str], length: int = 20) -> bytes:
        """Casts the informed key in to the 20 bytes key format. If the informed key has a 
        bytes type, the casted key will have the same bytes, but with b'\x00' padding bytes
        added. If the informed key has str type, the casted key will interpret the string as
        representing the hexadecimal digits and add the necessary b'\x00' padding bytes.

        Args:
            key (Union[bytes, str]): the informed key, as hex str or bytes
            length (int, optional): the length in bytes of the casted key. Defaults to 20.

        Returns:
            bytes: the casted key
        
        Examples:
            >>> key = cast_key_to_bytes('a3 12')
            >>> print(key)
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa3\x12'
            
            >>> key = cast_key_to_bytes(b'\xC5\x6A\x49\x2F')
            >>> print(key)
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x03\x02\x01'
            
        """
        key_bytes: bytes = None
        
        # informed key in bytes format
        if type(key) == bytes: key_bytes = key
        
        # informed key in hex string format
        if type(key) == str: key_bytes = bytes.fromhex(key)
        
        # adding padding
        padding_size = length - len(key_bytes)
        if padding_size > 0:
            padding = padding_size * b'\x00'
            key_bytes = padding + key_bytes
            
        return key_bytes
    
    
    def generate_key(length: int = 20, byte_order: Literal['little', 'big'] = 'big') -> bytes:
        """Generates a cryptographically strong pseudo-random secret key, with 20 bytes of length by default 
        (size of SHA1 used on the HMAC-SHA1).

        Args:
            length (int, optional): the length, in bytes, of the secret key. Defaults to 20.
            byte_order (Literal['little', 'big'], optional): the endianness of the bytes. Defaults to 'big'.

        Returns:
            bytes: the new pseudo-random secret key
        """
        bits_length = 8 * length
        random_int = secrets.randbits(bits_length)
        encoded_int = random_int.to_bytes(
            length=length,
            byteorder=byte_order,
            signed=False
        )
        return encoded_int
    
    
    def get_hex_str(key: bytes) -> str:
        """From a given key, as bytes, generates a hexadecimal str, with hex digits in pairs. For example,
        if the input key is b'\x9c\xd0\xdf\xbf\xf5Pns\t\xb7%\xe1+8\xe9\x02\x1f\x9b\xc6\x8d', then the
        hex_str will be '9c d0 df bf f5 50 6e 73 09 b7 25 e1 2b 38 e9 02 1f 9b c6 8d'.

        Args:
            key (bytes): the key in bytes

        Returns:
            str: the hex str
        
        Examples:
            >>> hex_str = get_hex_str(b'\x9c\xd0\xdf\xbf\xf5Pns\t\xb7%\xe1+8\xe9\x02\x1f\x9b\xc6\x8d')
            >>> print(hex_str)
            9c d0 df bf f5 50 6e 73 09 b7 25 e1 2b 38 e9 02 1f 9b c6 8d
        """
        hex_str = ''.join(f'{byte:02x} ' for byte in key)
        return hex_str
    
    
    def __str__(self):
        return SecretKey.get_hex_str(self.value)