# flask_util
Tools to decode and crack flask session encoded cookie

Cookies have the following format:

eyJfZmxhc2hlcyI6W3siIGRpIjp7IiB0X18iOlsibWVzc2FnZSIsIlBsZWFzZSBsb2cgaW4gdG8gYWNjZXNzIHRoaXMgcGFnZS4iXX19XX0.XqwoIA.TzwbrYVtTnZrttEZXCPODjhARBg

=> The first part (before .) contain json encoded in base64 format
=> The second part contain a timestamp encoded in base64 format
=> The last part contain an HMac signature



.eJwdisEKgCAQBX9leefoA_yK7iKy2KaCZbDexH_PPM3ATIe_CmsShbEddGaYBe-XtJ8Wt6hyFGw4irAKlRopP9QqcQgzUktZ6Z3PDjfGcOMDLjMeHA.XqwoIA.MYvHl4W55MChmAIZRxkWdAXCxn8

=> The first part (before .) contain json compressed (zlib) then encoded in base64 format
=> The second part contain a timestamp encoded in base64 format
=> The last part contain an HMac signature

# Requirements

This tools needs python3

# Installation
```
git clone https://github.com/mprunet/flask_util.git
cd flask_util
```

Create a virtual environment dedicated in order to keep your linux clean (Optional):
```sh
python3 -m venv flask-util-env
```

Activate your environment
```sh
source flask-util-env/bin/activate
```

Install flask
```sh
pip install flask
```

# Decode Session:
Extract your cookie from HTTP:

```
user@kali:~/flask_util/python decode.py .eJy9kM9OwzAMxl8ly3lCaeL821MgOHBA0-QmTlvRtajONKFp707gwI0b4mRZ_r7PP_smT2VGHonl4fUmRW1FnokZB5J7-TgTMol5HcS0iLoKTKkNRR0nFu9N8yCP9_3f-Z5omLhuWKd1Ec-Xb1O5zDvxQnNazyTO67T7ZSUyX9ctiyuySCMuA2XBPxHzxz-TVuL6hXrctxdvxKM8FJyZWjtleZDOAqTYh0S9xV6nqLUKJXQho_FUwAaE3IMBn52iEIM2uU86uZy0cQHAk3beB8gqonVOe1805oh90ZmMNioEiGQVGlAOLEYN0Hm0MZvYWdtuSLyVU13faGk8FLvgvKKYyHa5byIXkNC2REqgQkcdYIIs758pxrMs.Xqwd5g.oIUztGA_RLVRAZRZzq2nRUpBrX4

Your cookie is compressed with zlib
b'{"_flashes":[{" t":["message","Please log in to access this page."]},{" t":["message","Please log in to access this page."]},{" t":["message","Registration Successful! Welcome moi!"]},{" t":["message","Password was changed successfully"]},{" t":["message","Please log in to access this page."]},{" t":["message","Registration Successful! Welcome test!"]}],"_fresh":false,"_id":"6544c9b8ceb5ab2c92208f818da37ef458a4db4347d60e89823dbc2c6dc2368447e267784d09a566277f2ad9abf2de32308849e50a340645a924417a59d39155","csrf_token":"e918670e9ce51dbd3968aea5d9aec4081e14ac4d"}'
2020-05-01 13:02:30+00:00
SHA1 HMAC: a08533b4603f44b551019459ceada7454a41ad7e
```

# Brute force HMAC Key
```
user@kali:~/flask_util$ python bruteforce.py .eJwdisEKgCAQBX9leefoA_yK7iKy2KaCZbDexH_PPM3ATIe_CmsShbEddGaYBe-XtJ8Wt6hyFGw4irAKlRopP9QqcQgzUktZ6Z3PDjfGcOMDLjMeHA.XqwnVA.HgsSoKDefYAToB3Sv-JQAhpDG_0 /tmp/rockyou.txt 
Secret key: 0000000                
```

The script is configured for SHA1 HMac, you can change this behaviour in the source code
```
                signer_kwargs={
                    'key_derivation': 'hmac',
                    'digest_method' : hashlib.sha1
                    })
```

