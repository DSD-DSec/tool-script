import json
import subprocess
from flask import Flask
from flask import request
from datetime import datetime

app = Flask(__name__)


# POST request
@app.post("/gitleaks")
def run_gitleaks():
    # Link is taken from body parameters
    param = request.json
    link = param['link']

    # Name of pulled repository
    repo_name = link.split("/")[len(link.split("/")) - 1].split(".")[0]

    # Timestamp
    ts = str(datetime.now()).split()[1]

    # Directory and file name
    directory_name = ts
    file_name = 'output' + ts + '.json'

    # A new shell is opened in order to clone the repository, saving it in a directory called timestamp
    subprocess.run(['git clone ' + link + ' ' + directory_name, '-l'], shell=True)

    # A new shell is opened in order to run the tool to analyse all the pulled repository
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
