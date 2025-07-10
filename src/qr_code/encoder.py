from enum import Enum
from typing import *
from datetime import datetime

class Encoder:
    def encode_id(id: int, length: int = 4, byte_order: Literal['little', 'big'] = 'big') -> bytes:
        """Encodes a given id in to bytes, as an integer of 32 bits by default.

        Args:
            id (int): the input id
            length (int, optional): the length of the bytes array. Defaults to 4.
            byte_order (Literal['little', 'big'], optional): the endianness of the array of bytes. 
            Defaults to 'big'.
            
        Returns:
            bytes: the encoded id 
        """
        encoded_id = Encoder.encode_int(input_int=id, length=length, byte_order=byte_order)
        return encoded_id
    
    
    def encode_time(
        time: datetime,
        length: int = 8,
        byte_order: Literal['little', 'big'] = 'big'
    ) -> bytes:
        """Encodes a given timestamp in to bytes, representing the POSIX timestamp as an 64 bits integer,
        by default.

        Args:
            time (datetime): the input timestamp
            length (int, optional): the length of the bytes array. Defaults to 8.
            byte_order (Literal['little', 'big'], optional): the endianness of the array of bytes. 
            Defaults to 'big'.

        Returns:
            bytes: the encoded timestamp as POSIX
        """
        encoded_time = time.timestamp()
        encoded_time = int(encoded_time)
        encoded_time = encoded_time.to_bytes(
            length=length,
            byteorder=byte_order,
            signed=False
        )
        return encoded_time
    
    
    def encode_int(input_int: int, length: int = 4, byte_order: Literal['little', 'big'] = 'big') -> bytes:
        """Encodes a given input int in to bytes, as an integer of 32 bits by default.

        Args:
            input_int (int): the input int
            length (int, optional): the length of the bytes array. Defaults to 4.
            byte_order (Literal['little', 'big'], optional): the endianness of the array of bytes. 
            Defaults to 'big'.
            
        Returns:
            bytes: the encoded int
        """
        encoded_int = input_int.to_bytes(
            length=length,
            byteorder=byte_order,
            signed=False
        )
        return encoded_int