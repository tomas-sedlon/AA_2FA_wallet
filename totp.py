import base64
import hmac
import struct
import time


def hotp(key, counter, digits=6, digest='sha1'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)


def totp(key, unix_timestamp=time.time(), time_step=30, digits=6, digest='sha1'):
    return hotp(key, int(unix_timestamp / time_step), digits, digest)



# totp("ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS", 1686324381)


# fisrt 32 bytes is the code, second 32 bytes is the timestamp for a 64 byte result