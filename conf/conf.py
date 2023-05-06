import os

OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
OPEN_API_KEY_GPT4 = os.environ.get('OPEN_API_KEY_GPT4')
DEVICE_ID_AES_KEY = os.environ.get('DEVICE_ID_AES_KEY')
RSA_PUBLIC = open('./conf/rsa_public', 'r').read()
RSA_PRIVATE = open('./conf/rsa_private', 'r').read()
