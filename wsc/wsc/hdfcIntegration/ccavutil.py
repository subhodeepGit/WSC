#!/usr/bin/env python

from Crypto.Cipher import AES
import hashlib

def pad(data):
	length = 16 - (len(data) % 16)
	data += chr(length)*length
	return data


def encrypt(plainText,workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode())
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText.encode()).hex()
    return encryptedText



def decrypt(cipherText,workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode())
    encryptedText = bytes.fromhex(cipherText)
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    decryptedText = dec_cipher.decrypt(encryptedText)
    return str(decryptedText)

