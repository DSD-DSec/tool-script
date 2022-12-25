import json
import subprocess
import os

from flask import Flask, request
from datetime import datetime

import util
import os

app = Flask(__name__)

# POST request
@app.post("/gokart")
def run_gokart():
    # Taking request parameters
    param = request.json
    full_repo_name = param['repo']
    token = param['token']

    # Password used to generate the secret key and decrypt the token
    password = os.environ['PASS']    # password is retrieved from environment variables
    decrypted_token = util.decrypt(password, token)

    link = "https://" + decrypted_token + "@github.com/" + full_repo_name + ".git"

    # Timestamp
    ts = str(datetime.now()).split()[1]

    # Local directory and file name
    directory_name = ts
    file_name = 'output' + ts + '.json'

    # A new shell is opened in order to clone the repository, saving it in a directory called timestamp
    subprocess.run(['git clone ' + link + ' ' + directory_name, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the file inside the pulled repository
    output = subprocess.run(
        ['gokart scan -j -o ' + file_name + ' ' + directory_name + '/'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    print(output, flush=True)

    output = subprocess.run(
        ['ls'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    print(output, flush=True)

    # The analysis result is taken from the json file
    out = open(file_name)
    parsed = json.load(out)

    # Deletion of output file and pulled repository
    subprocess.run(['rm ' + file_name], shell=True)
    subprocess.run(['rm -r ' + directory_name], shell=True)

    # The json result is returned
    return parsed

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
