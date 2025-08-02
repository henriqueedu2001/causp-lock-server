from datetime import datetime
from qr_code.encoder import *
from auth.signer import Signer
from auth.secret_key import SecretKey
import segno    

class QRCode:
    def __init__(self, payload: str):
        self.payload = payload
        self.qrcode = None
        self.make_qrcode()
    
    
    def make_qrcode(self):
        """Generates the QR Code from the given payload
        """
        self.qrcode = segno.make_qr(self.payload)
        
    
    def save_qrcode(self, path: str, scale: int = 25, border: int = 5):
        """Saves the QR Code on the given path.

        Args:
            path (str): the path to save the QR Code.
            scale (int, optional): the scale of the QR Code. Defaults to 5.
            border (int, optional): the border size of the QR Code. Defaults to 0
        """
        self.qrcode.save(path, scale=scale, border=border)
    
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'raw payload: {self.get_payload_hex_str()}'
        return print_str
    
    
    def get_payload_hex_str(self):
        payload_hex_str = ''.join(f'{byte:02x} ' for byte in self.payload)
        return payload_hex_str
        

class QRCODE_CHECK_IN(QRCode):
    def __init__(self, user_id: int, generated_at: datetime, access_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_check_in_payload(
            user_id=user_id,
            generated_at=generated_at,
            access_key=access_key
        )
        self.user_id = user_id
        self.generated_at = generated_at
        self.access_key = access_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: CHECK_IN\n'
        print_str += f'user_id: {self.user_id}\n'
        print_str += f'generated_at: {self.generated_at}\n'
        print_str += f'access_key: {self.access_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str


class QRCODE_CHECK_OUT(QRCode):
    def __init__(self, user_id: int, generated_at: datetime, access_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_check_out_payload(
            user_id=user_id,
            generated_at=generated_at,
            access_key=access_key
        )
        self.user_id = user_id
        self.generated_at = generated_at
        self.access_key = access_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: CHECK_OUT\n'
        print_str += f'user_id: {self.user_id}\n'
        print_str += f'generated_at: {self.generated_at}\n'
        print_str += f'access_key: {self.access_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_BI_ACCESS(QRCode):
    def __init__(self, user_id: int, generated_at: datetime, access_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_bi_access_payload(
            user_id=user_id,
            generated_at=generated_at,
            access_key=access_key
        )
        self.user_id = user_id
        self.generated_at = generated_at
        self.access_key = access_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: BI_ACCESS\n'
        print_str += f'user_id: {self.user_id}\n'
        print_str += f'generated_at: {self.generated_at}\n'
        print_str += f'access_key: {self.access_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_SET_TIME(QRCode):
    def __init__(self, current_time: datetime, sync_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_set_time_payload(
            sync_time=current_time,
            sync_key=sync_key
        )
        self.sync_time = current_time
        self.sync_key = sync_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: SET_TIME\n'
        print_str += f'sync_time: {self.sync_time}\n'
        print_str += f'sync_key: {self.sync_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_SET_MASTER_KEY(QRCode):
    def __init__(self, new_master_key: Union[SecretKey, bytes], master_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_set_master_key_payload(
            new_master_key=new_master_key,
            old_master_key=master_key
        )
        self.new_master_key = new_master_key
        self.old_master_key = master_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: SET_MASTER_KEY\n'
        print_str += f'new_master_key: {self.new_master_key}\n'
        print_str += f'old_master_key: {self.old_master_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_SET_CONFIG_KEY(QRCode):
    def __init__(self, new_config_key: Union[SecretKey, bytes], master_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_set_config_key_payload(
            new_config_key=new_config_key,
            master_key=master_key
        )
        self.new_config_key = new_config_key
        self.master_key = master_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: SET_CONFIG_KEY\n'
        print_str += f'new_config_key: {self.new_config_key}\n'
        print_str += f'master_key: {self.master_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_SET_SYNC_KEY(QRCode):
    def __init__(self, new_sync_key: Union[SecretKey, bytes], config_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_set_sync_key_payload(
            new_sync_key=new_sync_key,
            config_key=config_key
        )
        self.new_sync_key = new_sync_key
        self.config_key = config_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: SET_SYNC_KEY\n'
        print_str += f'new_sync_key: {self.new_sync_key}\n'
        print_str += f'config_key: {self.config_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_SET_ACCESS_KEY(QRCode):
    def __init__(self, new_access_key: Union[SecretKey, bytes], config_key: Union[SecretKey, bytes]):
        self.payload = PayloadEncoder.get_set_access_key_payload(
            new_access_key=new_access_key,
            config_key=config_key
        )
        self.new_access_key = new_access_key
        self.config_key = config_key
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: SET_ACCESS_KEY\n'
        print_str += f'new_access_key: {self.new_access_key}\n'
        print_str += f'config_key: {self.config_key}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_BLINK_N_TIMES(QRCode):
    def __init__(self, blink_num: int):
        self.payload = PayloadEncoder.get_blink_n_times_payload(
            blink_num=blink_num
        )
        self.blink_num = blink_num
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: BLINK_N_TIMES\n'
        print_str += f'blink_num: {self.blink_num}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str

    
class QRCODE_BLINK_IF_SYNC(QRCode):
    def __init__(self, current_time: datetime):
        self.payload = PayloadEncoder.get_debug_sync_payload(
            current_time=current_time
        )
        self.current_time = current_time
        self.qrcode = None
        self.make_qrcode()
        pass
    
    def __str__(self):
        print_str = f'QR Code Info\n'
        print_str += f'action: BLINK_IF_SYNC\n'
        print_str += f'current_time: {self.current_time}\n'
        print_str += f'payload: {self.get_payload_hex_str()}'
        return print_str