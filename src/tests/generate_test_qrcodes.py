from enum import Enum
from datetime import datetime
from qr_code.generator import *
from qr_code.encoder import *
from auth.signer import Signer
from auth.secret_key import SecretKey

access_key = SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')
sync_key = SecretKey('bf 42 9e 35 29 c5 f1 4e bb 81 8c 15 a3 cd 98 04 f6 1d 4b 98')
master_key = SecretKey('9f 96 5e 25 bb ba 22 eb 9e 3f a1 32 98 11 92 1e e0 d9 b2 2e')
config_key = SecretKey('79 31 8f 33 5e 6b f5 37 b9 b6 2e 56 ac 54 f8 36 f4 58 f9 db')
generic_secret_key = SecretKey('cc 93 ec 5e 31 98 c4 22 0a 39 44 a9 01 36 2f 33 12 10 a3 5f')

qrcode_check_in = QRCODE_CHECK_IN(
    user_id=2305947582,
    generated_at=datetime(year=2025, month=7, day=17, hour=15, minute=14),
    access_key=SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')
)

qrcode_check_out = QRCODE_CHECK_OUT(
    user_id=2305947582,
    generated_at=datetime(year=2025, month=7, day=17, hour=15, minute=18),
    access_key=SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')
)

qrcode_bi_access = QRCODE_BI_ACCESS(
    user_id=2305947582,
    generated_at=datetime(year=2025, month=7, day=17, hour=15, minute=18),
    access_key=SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')
)

qrcode_set_time = QRCODE_SET_TIME(
    current_time=datetime(year=2025, month=7, day=17, hour=14, minute=29),
    sync_key=SecretKey('bf 42 9e 35 29 c5 f1 4e bb 81 8c 15 a3 cd 98 04 f6 1d 4b 98')
)

qrcode_set_master_key = QRCODE_SET_MASTER_KEY(
    new_master_key=SecretKey('cc 93 ec 5e 31 98 c4 22 0a 39 44 a9 01 36 2f 33 12 10 a3 5f'),
    master_key=SecretKey('1a 50 63 d3 2c ec 63 93 40 f5 fb 9f c6 e1 7f f6 f3 d5 bf 70'),
)

qrcode_set_config_key = QRCODE_SET_CONFIG_KEY(
    new_config_key=SecretKey('e7 e5 00 11 c6 ff eb f0 ee a6 f9 47 e6 c5 43 bb c9 7e 42 db'),
    master_key=SecretKey('ed 5c 53 fe 28 c8 64 47 a0 33 dc a2 16 d7 51 6b 58 95 6c 34'),
)

qrcode_set_sync_key = QRCODE_SET_SYNC_KEY(
    new_sync_key=SecretKey('e7 e5 00 11 c6 ff eb f0 ee a6 f9 47 e6 c5 43 bb c9 7e 42 db'),
    config_key=SecretKey('24 39 d1 1b f3 ff 67 23 35 c4 ca 47 1d 77 2f c4 68 68 ed bf'),
)

qrcode_set_access_key = QRCODE_SET_ACCESS_KEY(
    new_access_key=SecretKey('e7 e5 00 11 c6 ff eb f0 ee a6 f9 47 e6 c5 43 bb c9 7e 42 db'),
    config_key=SecretKey('2c 19 31 79 8f 21 49 a1 f8 2f 2f 37 ba 82 b6 bd d1 69 34 f3'),
)

qrcode_blink_n_times = QRCODE_BLINK_N_TIMES(
    blink_num=4
)

qrcode_blink_if_sync = QRCODE_BLINK_IF_SYNC(
    current_time=datetime(year=2025, month=7, day=17, hour=15, minute=3)
)

qrcode_corrupted = QRCode(
    payload=b'\x00\x88\x71\xf7\xbe\x68\x79\x3d\x68\x56\x13\x24\xe0\x34\x23\xa7\xe2\xf0\x1b\x58\xb0\x17\xd3\x6b\x60\x16\xf7\x36\xd3'
)

print(f'{qrcode_check_in}\n')
print(f'{qrcode_check_out}\n')
print(f'{qrcode_bi_access}\n')
print(f'{qrcode_set_time}\n')
print(f'{qrcode_set_master_key}\n')
print(f'{qrcode_set_config_key}\n')
print(f'{qrcode_set_sync_key}\n')
print(f'{qrcode_set_access_key}\n')
print(f'{qrcode_blink_n_times}\n')
print(f'{qrcode_blink_if_sync}\n')
print(f'{qrcode_corrupted}')

qrcode_check_in.save_qrcode('./test_qrcodes/CHECK_IN.png')
qrcode_check_in.save_qrcode('./test_qrcodes/CHECK_OUT.png')
qrcode_bi_access.save_qrcode('./test_qrcodes/BI_ACCESS.png')
qrcode_set_time.save_qrcode('./test_qrcodes/SET_TIME.png')
qrcode_set_master_key.save_qrcode('./test_qrcodes/SET_MASTER_KEY.png')
qrcode_set_config_key.save_qrcode('./test_qrcodes/SET_CONFIG_KEY.png')
qrcode_set_sync_key.save_qrcode('./test_qrcodes/SET_SYNC_KEY.png')
qrcode_set_access_key.save_qrcode('./test_qrcodes/SET_ACCESS_KEY.png')
qrcode_blink_n_times.save_qrcode('./test_qrcodes/BLINK_N_TIMES.png')
qrcode_blink_if_sync.save_qrcode('./test_qrcodes/BLINK_IF_SYNC.png')
qrcode_corrupted.save_qrcode('./test_qrcodes/CORRUPTED.png')
