import gzip
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from argparse import ArgumentParser
import binascii
from src import config
from dataclasses import dataclass


def read_iv_from_file(file_path):
    with open(file_path, "rb") as f:
        iv = f.read(16)
        if len(iv) != 16:
            raise Exception("Invalid file")
    return iv


def pad_data(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()


def remove_pkcs7_padding(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def decrypt_file(input_file, is_fumen):
    # Convert the key from hex to bytes
    key = binascii.unhexlify(config.config.fumenKey if is_fumen else config.config.datatableKey)

    # Read the IV from the first 16 bytes of the input file
    iv = read_iv_from_file(input_file)

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # except Exception as error:
    #     print(error)
    #     print("You need to set the right AES keys in the encryption.py file")
    #     exit(0)

    with open(input_file, "rb") as infile:
        # Skip the IV in the input file
        infile.seek(16)

        # Decrypt the file
        decrypted_data = b"" + decryptor.update(infile.read())

        # Remove PKCS7 padding
        unpadded_data = remove_pkcs7_padding(decrypted_data)

        # Gzip decompress the data
        decompressed_data = gzip.decompress(unpadded_data)

        # return the decompressed data
        return decompressed_data


def isJson(file: bytes):
    try:
        json.loads(file)
        return True
    except:
        return False


def encrypt_file(input_file, is_fumen):
    # Convert the key from hex to bytes
    key = binascii.unhexlify(config.config.fumenKey if is_fumen else config.config.datatableKey)

    # Generate a random 128-bit IV
    iv = os.urandom(16)

    # Create an AES cipher object with CBC mode
    # try:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # except Exception as error:
    #     print(error)
    #     print("You need to set the right AES keys in the encryption.py file")
    #     exit(0)

    with open(input_file, "rb") as infile:
        # Read the entire file into memory
        data = infile.read()

        # Gzip compress the data
        compressed_data = gzip.compress(data)

        # Pad the compressed data, encrypt it, and return the encrypted result
        encrypted_data = (
            encryptor.update(pad_data(compressed_data)) + encryptor.finalize()
        )

    return iv + encrypted_data


def save_file(file: bytes, outdir: str, encrypt: bool, is_fumen: bool = False):
    fileContent = (
        decrypt_file(input_file=file, is_fumen=is_fumen)
        if not encrypt
        else encrypt_file(input_file=file, is_fumen=is_fumen)
    )

    if isJson(fileContent):
        base = os.path.splitext(outdir)[0]
        outdir = base + ".json"
    else:
        base = os.path.splitext(outdir)[0]
        outdir = base + ".bin"

    print("Decrypting" if not encrypt else "Encrypting", file, "to", outdir)

    with open(outdir, "wb") as outfile:
        outfile.write(fileContent)