from enum import Enum
from typing import *
from datetime import datetime
from auth.secret_key import SecretKey
from auth.signer import Signer

class MessageTypes(Enum):
    ACCESS = 0
    SYNC = 1
    CONFIG = 2
    DEBUG = 3


class OperationTypes(Enum):
    CHECK_IN = 0
    CHECK_OUT = 1
    SET_MASTER_KEY = 2
    SET_CONFIG_KEY = 3
    SET_SYNC_KEY = 4
    SET_ACCESS_KEY = 5
    DEBUG_BLINK = 6
    DEBUG_SYNC = 7
    

class PrivateKeyTypes(Enum):
    MASTER_KEY = 0
    ACCESS_KEY = 1
    SYNC_KEY = 2
    CONFIG_KEY = 3


class PayloadEncoder:
    def __init__(self):
        pass


class PayloadHeaderEncoder:
    def get_header(message_type: Union[MessageTypes, int], operation: Union[OperationTypes, int]) -> bytes:
        """Generates the payload header, with a message type and an operation, in a single byte. In the header
        encoding, the 4 most significant bits are the message type  and the 4 less significant are the operation
        bits. For example, with the payload being message_type = 0 (ACCESS) and operation = 1 (CHECK_OUT), the 
        header will be header = 0x01 (hex) = 0000 0001 (bin).

        Args:
            message_type (Union[MessageTypes, int]): the message type
            operation (Union[OperationTypes, int]): the operation

        Returns:
            bytes: the encoded header
        """
        message_type_int = message_type.value if type(message_type) == MessageTypes else message_type
        operation_int = operation.value if type(operation) == OperationTypes else operation
        high_byte = (message_type_int << 4) & 240 # high_byte = (msg_type << 4) & 0xF0
        low_byte = operation_int & 15 # low_byte = op & 0x0F
        header = high_byte + low_byte
        header = header.to_bytes()
        return header


class PayloadBodyEncoder:
    def get_body(**kwargs) -> bytes:
        """Generates the payload body depending on the `message_type` specified in kwargs.

        The content of the body varies depending on the value of `message_type`:
        
        - For `MessageTypes.ACCESS`, provide:
            - `user_id` (int)
            - `generated_at` (datetime)
        - For `MessageTypes.SYNC`, provide:
            - `sync_time` (datetime)
        - For `MessageTypes.CONFIG`, provide:
            - `new_key` (str)
        - For `MessageTypes.DEBUG`, provide:
            - `debug_data` (str)

        Args:
            **kwargs: Arbitrary keyword arguments including:
                message_type (MessageTypes): The type of message.
                operation (OperationTypes, optional): Operation type, used for access messages.
                user_id (int, optional): User ID (required for ACCESS).
                generated_at (datetime, optional): Timestamp (required for ACCESS).
                sync_time (datetime, optional): Timestamp (required for SYNC).
                new_key (str, optional): New configuration key (required for CONFIG).
                debug_data (str, optional): Debug payload (required for DEBUG).

        Returns:
            bytes: The encoded payload body.

        Examples:
            >>> PayloadBodyEncoder.get_body(
            ...     message_type=MessageTypes.ACCESS,
            ...     operation=OperationTypes.CHECK_IN,
            ...     user_id=1902489364,
            ...     generated_at=datetime(2025, 5, 10, 21, 30)
            ... )
            b'qe\\xaf\\x14\\x00\\x00\\x00\\x00h\\x1f\\xef\\x88'

            >>> PayloadBodyEncoder.get_body(
            ...     message_type=MessageTypes.SYNC,
            ...     sync_time=datetime(2025, 5, 10, 21, 30)
            ... )
            b'\\x00\\x00\\x00\\x00h\\x1f\\xef\\x88'

            >>> PayloadBodyEncoder.get_body(
            ...     message_type=MessageTypes.CONFIG,
            ...     new_key='01 02 03 04 AA BB CC DD'
            ... )
            b'\\x00...\\xdd'

            >>> PayloadBodyEncoder.get_body(
            ...     message_type=MessageTypes.DEBUG,
            ...     debug_data='AA BB CC DD FF FF FF FF'
            ... )
            b'\\x00...\\xff'
        """

        message_type: Union[MessageTypes, int] = kwargs.get('message_type')
        
        body = None
        if message_type == MessageTypes.ACCESS:
            user_id: int = kwargs.get('user_id')
            generated_at: datetime = kwargs.get('generated_at')
            body = PayloadBodyEncoder.get_access_body(user_id=user_id, generated_at=generated_at)
        elif message_type == MessageTypes.SYNC:
            sync_time: datetime = kwargs.get('sync_time')
            body = PayloadBodyEncoder.get_sync_body(sync_time=sync_time)
        elif message_type == MessageTypes.CONFIG:
            new_key: str = kwargs.get('new_key')
            body = PayloadBodyEncoder.get_config_body(new_key=new_key)
        elif message_type == MessageTypes.DEBUG:
            debug_data: str = kwargs.get('debug_data')
            body = PayloadBodyEncoder.get_debug_body(debug_data=debug_data)
        
        return body
    
    
    def get_access_body(user_id: int, generated_at: datetime) -> bytes:
        """Generates the payload access body, with the given user id (4 bytes) and its
        generated_at timestamp (8 bytes).

        Args:
            user_id (int): the user id
            generated_at (datetime): the generated_at timestamp

        Returns:
            bytes: the encoded access payload body
        """
        user_id_bytes = BinaryEncoder.encode_id(user_id)
        generated_at_bytes = BinaryEncoder.encode_time(generated_at)
        body = user_id_bytes + generated_at_bytes
        return body
    
    
    def get_sync_body(sync_time: datetime) -> bytes:
        """Generates the payload sync body, with the sync_time encoded with
        8 bytes.

        Args:
            sync_time (datetime): the sync time

        Returns:
            bytes: the encoded sync payload body
        """
        sync_time_bytes = BinaryEncoder.encode_time(sync_time)
        body = sync_time_bytes
        return body
    
    
    def get_config_body(new_key: str) -> bytes:
        """Generates the payload config body, with the new_key
        encoded with 16 bytes.

        Args:
            new_key (str): the new key

        Returns:
            bytes: the encoded config payload body
        """
        new_key_bytes = bytes.fromhex(new_key)
        new_key_bytes = BinaryEncoder.encode_hex_str(new_key)
        body = new_key_bytes
        return body
    
    
    def get_debug_body(
        debug_data: Union[bytes, str],
        length: int = 32,
        byte_order: Literal['little', 'big'] = 'big'
    ) -> bytes:
        """Generates the debug payload body, with an array of 32 bytes.

        Args:
            debug_data (Union[bytes, str]): the debug data
            length (int, optional): the length of the bytes array. Defaults to 32.
            byte_order (Literal['little', 'big'], optional): the endianness of the array of bytes. Defaults to 'big'.

        Returns:
            bytes: the encoded debug data
        """
        debug_bytes = BinaryEncoder.encode_hex_str(
            input_hex_str=debug_data,
            length=length,
            byte_order=byte_order
        ) if type(debug_data) == str else debug_data
        return debug_bytes
    

class PayloadHashEncoder:
    def get_hash(header: bytes, body: bytes, private_key: Union[bytes, SecretKey]) -> bytes:
        """Generates the signature of the message (header + body), with HMAC-SHA1.

        Args:
            header (bytes): the payload header
            body (bytes): the payload body
            private_key (Union[bytes, SecretKey]): the private key

        Returns:
            bytes: the signature (HMAC-SHA1)
        """
        message = header + body
        key = private_key.value if type(private_key) == SecretKey else private_key
        hash = Signer.sign(message, key)
        return hash


class BinaryEncoder:
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
        encoded_id = BinaryEncoder.encode_int(input_int=id, length=length, byte_order=byte_order)
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
    
    
    def encode_hex_str(input_hex_str: str, length: int = 20, byte_order: Literal['little', 'big'] = 'big') -> bytes:
        """Encodes the given str, interpreted as a hexadecimal string, as an array of bytes, with
        a fixed length of 20, by default. The not empty space will be filled padding zeros.

        Args:
            input_hex_str (str): the input hex string
            length (int, optional): the array of bytes fixed length. Defaults to 20.
            byte_order (Literal['little', 'big'], optional): the endianness of the array of bytes. Defaults to 'big'.

        Returns:
            bytes: _description_
        """
        input_hex_str_bytes = bytes.fromhex(input_hex_str)
        padding_size = length - len(input_hex_str_bytes)
        if padding_size > 0:
            padding_bytes = padding_size * b'\x00'
            input_hex_str_bytes = padding_bytes + input_hex_str_bytes
        return input_hex_str_bytes
    
    
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