import json
import subprocess
from flask import Flask
from flask import request

app = Flask(__name__)


# POST request
@app.post("/gitleaks")
def run_gitleaks():
    # Link is taken from body parameters
    param = request.json
    link = param['link']

    # A new shell is opened in order to clone the repository
    subprocess.run(['git clone ' + link, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the pulled repository
    output = subprocess.run(
        ['gitleaks detect --no-git -r=output.json -s=' + link.split("/")[len(link.split("/")) - 1].split(".")[0], '-l'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # The output of the tool is saved
    result = output.stderr.decode('utf-8')
    result += output.stdout.decode('utf-8')

    # The analysis result is taken from the json file
    out = open("output.json")
    parsed = json.load(out)

    # The json result is returned 
    return parsed
