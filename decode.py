import sys

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
if len(sys.argv)!=2:
    print("Usage "+sys.argv[0]+" <cookie_value>")
    sys.exit(1)
from datetime import datetime
from datetime import timezone
import struct
import hashlib
import base64
import zlib

_int64_struct = struct.Struct(">Q")
_int_to_bytes = _int64_struct.pack
_bytes_to_int = _int64_struct.unpack
def want_bytes(s, encoding="utf-8", errors="strict"):
    if isinstance(s, str):
        s = s.encode(encoding, errors)

    return s

def int_to_bytes(num):
    return _int_to_bytes(num).lstrip(b"\x00")


def bytes_to_int(bytestr):
    return _bytes_to_int(bytestr.rjust(8, b"\x00"))[0]

payload=sys.argv[1]
decompress=False
if payload.startswith('.'):
    # base64 zlib
    decompress=True
    payload=payload[1:]
    print("Your cookie is compressed with zlib")

try:
    payloadA=payload.split('.')
    payloadA= [s + ("=" * ((4 - len(s) % 4) % 4)) for s in payloadA]

    json = base64.urlsafe_b64decode(payloadA[0])
    try:
        if decompress:
            json = zlib.decompress(json)
    except e:
        print("Impossible to decompress")
    print(json)
except:
    print('Impossible to decode the value, may be not a Flask Session')

try:
    ts = bytes_to_int(base64.urlsafe_b64decode(payloadA[1]))
    try:
        print(datetime.fromtimestamp(ts, tz=timezone.utc))
    except:
        print("Timestamp cannot be converted in date " + ts)
except:
    print('Impossible to decode the timestamp')
    print(payloadA[1])
sign=payloadA[2]
try:
    sign = base64.urlsafe_b64decode(payloadA[2])
    if len(sign)==20:
        print("SHA1 HMAC: " + sign.hex())
    else:
        size=len(sign)*8
        print('SHA'+str(size)+' HMAC: ' + sign.hex())
except:
    print('Impossible to decode the signature ')
    print(sign)


