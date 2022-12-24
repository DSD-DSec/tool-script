import base64
import hashlib
from Cryptodome.Cipher import AES

HASH_NAME = "SHA256"
IV_LENGTH = 12
ITERATION_COUNT = 65536
KEY_LENGTH = 32
SALT_LENGTH = 100
TAG_LENGTH = 16


# Algorithm used -> AES/GCM/NoPadding, PBKDF2WithHmacSHA256
# Function used to obtain the secret key according to the algorithm used
def get_secret_key(password, salt):
    return hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATION_COUNT, KEY_LENGTH)


# Function used to decrypt the received token
def decrypt(password, cipher_message):
    # Decode of cipher text
    decoded_cipher_byte = base64.b64decode(cipher_message)

    # Splitting the decoded cipher in iv, salt, message and tag
    iv = decoded_cipher_byte[:IV_LENGTH]
    salt = decoded_cipher_byte[IV_LENGTH:(IV_LENGTH + SALT_LENGTH)]
    encrypted_message_byte = decoded_cipher_byte[(IV_LENGTH + SALT_LENGTH):-TAG_LENGTH]
    tag = decoded_cipher_byte[-TAG_LENGTH:]

    # Computation of secret key using password and salt
    secret = get_secret_key(password, salt)
    cipher = AES.new(secret, AES.MODE_GCM, iv)

    # Decrypt and return message
    decrypted_message_byte = cipher.decrypt(encrypted_message_byte)
    return decrypted_message_byte.decode("utf-8")