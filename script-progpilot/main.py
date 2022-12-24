import json
import subprocess
import os

from flask import Flask, request
from datetime import datetime

import util
import os

app = Flask(__name__)


# POST request
@app.post("/progpilot")
def run_progpilot():
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

    # A new shell is opened in order to clone the repository, saving it in a directory called timestamp
    subprocess.run(['git clone ' + link + ' ' + directory_name, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the file inside the pulled repository
    output = subprocess.run(
        ['progpilot ' + directory_name + '/'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    # The output of the tool is saved
    result = output.stderr
    result += output.stdout
    
    # Clean up progpilot results
    result = result.replace(" ", "")
    result = result.replace("\n", "")
    index = result.find("[{")
    
    if index != -1:
        result = result[index:]

    # Deletion of output file and pulled repository
    subprocess.run(['rm -r ' + directory_name], shell=True)

    # The json result is returned
    try:
        return json.loads(result)
    except:
        return json.loads("[]")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
