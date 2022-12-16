import json
import subprocess
import os

from flask import Flask
from flask import request
from datetime import datetime

import util

app = Flask(__name__)

# POST request
@app.post("/gokart")
def run_gokart():
    # Taking request parameters
    param = request.json
    username = param['user']
    repository = param['repo']
    token = param['token']

    # Password used to generate the secret key and decrypt the token
    password = os.environ['PASS']    # password is retrieved from environment variables
    decrypted_token = util.decrypt(password, token)

    link = "https://" + decrypted_token + "@github.com/" + username + "/" + repository + ".git"

    # Timestamp
    ts = str(datetime.now()).split()[1]

    # Local directory and file name
    directory_name = ts
    file_name = 'output' + ts + '.json'

    # A new shell is opened in order to clone the repository, saving it in a directory called timestamp
    subprocess.run(['git clone ' + link + ' ' + directory_name, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the file inside the pulled repository
    subprocess.run(
        ['gokart scan -j -o ' + file_name + ' ' + directory_name + '/'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # The analysis result is taken from the json file
    out = open(file_name)
    parsed = json.load(out)

    # Deletion of output file and pulled repository
    subprocess.run(['rm ' + file_name], shell=True)
    subprocess.run(['rm -r ' + directory_name], shell=True)

    # The json result is returned
    return parsed