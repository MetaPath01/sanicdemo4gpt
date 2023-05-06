import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


def encrypt_ecb_pkcs7(key, plaintext):
    try:
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size, style='pkcs7')
        ciphertext = cipher.encrypt(padded_plaintext)
        return base64.b64encode(ciphertext).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {e}")
        return ""


def decrypt_ecb_pkcs7(key, ciphertext_base64):
    try:
        ciphertext = base64.b64decode(ciphertext_base64)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size, style='pkcs7')
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e} wrong key: {key}")
        return ""
