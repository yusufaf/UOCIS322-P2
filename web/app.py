"""
Yusuf Afzal's Flask API.
"""
from flask import (Flask, request, render_template, Response, abort)
import sys      # Used for printing because regular print() doesn't work 
import os.path  # Used for determining if file path is valid
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)
log = logging.getLogger(__name__)

import configparser    # Configure from .ini files and command line
from configparser import ConfigParser
config = configparser.ConfigParser()
config.read("./app.ini")
                           
global DOCROOT
DOCROOT = config['DEFAULT'].get('DOCROOT')

app = Flask(__name__)   

# Possibly helpful?: https://stackoverflow.com/questions/21310147/catch-all-path-in-flask-app
@app.route("/<path:path>") # route() tells Flask what URL should trigger function
def respond(path):  
    path = DOCROOT + path   # Prepends DOCROOT "./" to the path
    if '~' in path or '//' in path or '..' in path: # Disallowed symbols, respond with 403
        abort(403)
    elif not os.path.exists(path):  # Path doesn't exist, respond with 404
        abort(404)
    else:  # Otherwise, the file exists:
        if os.path.isfile(path):    # Checking if it's a file, previous if checks for existence
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200     # Send file content with 200 OK HTTP code
    
    return "That request is not handled", 401   # 401 was Not Implemented from proj1


# Error handler for 403 Forbidden, use abort() to invoke this handler in respond()
@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403     

# Error handler for 404 Not Found, use abort() to invoke this handler in respond()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  

