import gzip
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from argparse import ArgumentParser
from enum import Enum
import binascii
from src import config


class Keys(Enum):
    Datatable = config.config.datatableKey
    Fumen = config.config.fumenKey


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


def decrypt_file(input_file, key_type: Keys = Keys(Keys.Datatable)):
    # Convert the key from hex to bytes
    key = binascii.unhexlify(Keys(key_type.value).value)

    # Read the IV from the first 16 bytes of the input file
    iv = read_iv_from_file(input_file)

    try:
        # Create an AES cipher object with CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
    except Exception as error:
        print(error)
        print("You need to set the right AES keys in the encryption.py file")
        exit(0)

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


def encrypt_file(input_file, key_type: Keys = Keys(Keys.Datatable)):
    # Convert the key from hex to bytes
    key = binascii.unhexlify(Keys(key_type.value).value)

    # Generate a random 128-bit IV
    iv = os.urandom(16)

    # Create an AES cipher object with CBC mode
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
    except Exception as error:
        print(error)
        print("You need to set the right AES keys in the encryption.py file")
        exit(0)

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


def save_file(file: bytes, outdir: str, encrypt: bool):
    fileContent = (
        decrypt_file(input_file=file, key_type=type)
        if not encrypt
        else encrypt_file(input_file=file, key_type=type)
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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Input file / folder",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file / folder",
    )
    parser.add_argument(
        "-e",
        "--enc",
        action="store_true",
        default=False,
        help="Use this flag to encrypt a file",
    )
    parser.add_argument(
        "-t",
        "--fumen",
        action="store_true",
        default=False,
        help="Datatable is default, use this flag for Fumen",
    )
    args = parser.parse_args()

    if not args.input:
        print("Missing input file, pass the argument --help for help")
        exit(0)

    if not args.output:
        print("Missing output file, pass the argument --help for help")
        exit(0)

    type = Keys.Datatable if not args.fumen else Keys.Fumen

    if os.path.isdir(args.input):
        for path, subdirs, files in os.walk(args.input):
            for name in files:
                full_path = os.path.join(path, name)
                relative_path = os.path.relpath(full_path, args.input)
                outpath = os.path.join(args.output, relative_path)
                outdir = os.path.dirname(outpath)

                Path(outdir).mkdir(parents=True, exist_ok=True)

                if os.path.isfile(full_path):
                    save_file(
                        file=full_path,
                        outdir=outpath,
                        encrypt=False if not args.enc else True,
                    )

    else:
        save_file(
            file=args.input,
            outdir=args.output,
            encrypt=False if not args.enc else True,
        )
