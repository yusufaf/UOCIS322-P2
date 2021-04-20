"""
Yusuf Afzal's Flask API.
"""

from flask import (Flask, request, 
                  render_template, Response, 
                  abort, make_response)
                # request has data like the requested URL
                # render_template provides for the response

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

import configparser    # Configure from .ini files and command line
from configparser import ConfigParser
config = configparser.ConfigParser()
config.read("./credentials.ini")
global port                      # Better way to do this instead of globals?
port = config['DEFAULT']['port']

global DOCROOT
DOCROOT = config['DEFAULT']['DOCROOT']


import sys      # Used for printing because regular print() doesn't work 
import os.path  # Used for determining if file path is valid

app = Flask(__name__,                   # template_folder="templates", static_folder="static"
            template_folder="templates")   

# https://stackoverflow.com/questions/21310147/catch-all-path-in-flask-app
# This allows us to handle all paths from just a single route / method

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>") # route() tells Flask what URL should trigger function
def respond(path):  # Searching from root or having the <path> variable
    log.info("\n--- Received request ----")
    log.info("Request URL was {}\n***\n".format(request.url))

    path = DOCROOT + path   # Prepends the DOCROOT (./) to the path

    log.info("PORT is " + port)
    log.info("PATH IS " + path)

    # TODO: Figure out whether having the 404.html in the templates directory is fine
    if '~' in path or '//' in path or '..' in path: # Disallowed symbols, respond with 403
        abort(403)
    elif not os.path.exists(path):  # Path does not exist, respond with 404
        abort(404)
    else:  # Otherwise, the file exists:
        if os.path.isfile(path):    # Checking whether it's a file, because other checks for existence
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200     # Transmit content of file with a 200 OK HTTP code
    
    return "That request is not handled", 401   # 401 was Not Impelemented from proj1


# Error handler for 403 Error, use abort() command to call this handler in respond()
@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403     

# Error handler for 404 Error, use abort() command to call this handler in respond()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)  # port = port, passing in from credentials

