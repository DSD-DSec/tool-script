import json
import subprocess
import os

from flask import Flask
from flask import request
from datetime import datetime

import base64
import hashlib
from Cryptodome.Cipher import AES

HASH_NAME = "SHA256"
IV_LENGTH = 12
ITERATION_COUNT = 65536
KEY_LENGTH = 32
SALT_LENGTH = 100
TAG_LENGTH = 16

app = Flask(__name__)


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


# POST request
@app.post("/gitleaks")
def run_gitleaks():
    # Taking request parameters
    param = request.json
    username = param['user']
    repository = param['repo']
    token = param['token']

    # Password used to generate the secret key and decrypt the token
    password = os.environ['PASS']    # password is retrieved from environment variables
    decrypted_token = decrypt(password, token)

    print(decrypted_token)

    link = "https://" + decrypted_token + "@github.com/" + username + "/" + repository + ".git"

    # Timestamp
    ts = str(datetime.now()).split()[1]

    # Local directory and file name
    directory_name = ts
    file_name = 'output' + ts + '.json'

    # A new shell is opened in order to clone the repository, saving it in a directory called timestamp
    subprocess.run(['git clone ' + link + ' ' + directory_name, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the file inside the pulled repository
    output = subprocess.run(
        ['gitleaks detect --no-git -r=' + file_name + ' -s=' + directory_name, '-l'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # The output of the tool is saved
    result = output.stderr.decode('utf-8')
    result += output.stdout.decode('utf-8')

    # The analysis result is taken from the json file
    out = open(file_name)
    parsed = json.load(out)

    # Deletion of output file and pulled repository
    subprocess.run(['rm ' + file_name], shell=True)
    subprocess.run(['rm -r ' + directory_name], shell=True)

    # The json result is returned 
    return parsed
