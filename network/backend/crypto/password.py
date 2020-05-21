from binascii import hexlify
from hashlib import sha256, pbkdf2_hmac
from os import urandom

HASH_NAME = 'sha512'
HASH_ITERATIONS = 1000


def hash_password(raw_password: str) -> str:
    salt = sha256(urandom(60)).hexdigest().encode('ascii')
    password = pbkdf2_hmac(
        hash_name='sha512',
        password=raw_password.encode('utf-8'),
        salt=salt,
        iterations=HASH_ITERATIONS,
    )

    return (salt + hexlify(password)).decode('ascii')


def verify_password(db_password: str, test_password: str) -> bool:
    password = pbkdf2_hmac(
        hash_name='sha512',
        password=test_password.encode('utf-8'),
        salt=db_password[:64].encode('ascii'),
        iterations=HASH_ITERATIONS,
    )

    return hexlify(password).decode('ascii') == db_password[64:]
