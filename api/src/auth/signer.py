import hmac
import hashlib

class Signer:
    def sign(message: bytes, key: bytes) -> bytes:
        """Signs the message with HMAC-SHA1

        Args:
            message (bytes): the bytes of the message
            key (bytes): the secret key

        Returns:
            bytes: the signature, as bytes
        """
        hmac_obj = hmac.new(key, message, hashlib.sha1)
        signature = bytes(hmac_obj.digest())
        return signature
    
    
    def verify_signature(message: bytes, key: bytes, received_signature: bytes) -> bool:
        """Verifies if the signature of the message is valid, with HMAC-SHA1

        Args:
            message (bytes): the received message
            key (bytes): the secret key
            received_signature (bytes): the received signature

        Returns:
            bool: _description_
        """
        hmac_obj = hmac.new(key, message, hashlib.sha1)
        expected_signature = hmac_obj.digest()
        validity = hmac.compare_digest(expected_signature, received_signature)
        return validity