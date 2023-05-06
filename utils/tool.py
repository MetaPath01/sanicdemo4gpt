import rsa
import base64


# rsa加密
def rsa_encrypt(content, publicKey):
    public_key = rsa.PublicKey.load_pkcs1(publicKey.encode('utf-8'))
    crypto = rsa.encrypt(content.encode('utf-8'), public_key)
    return crypto


# rsa解密
def rsa_decrypt(content_base64, privateKey):
    try:
        crypto_tra = base64.decodebytes(content_base64.encode('utf-8'))
        pri = rsa.PrivateKey.load_pkcs1(privateKey.encode('utf-8'))
        content = rsa.decrypt(crypto_tra, pri)
        con = content.decode("utf-8")
    except Exception as e:
        print("rsaDecrypt 解密失败 ", content_base64, e)
        return ""

    return con
