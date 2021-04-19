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
global port
port = config['DEFAULT']['port']


import sys      # Used for printing because regular print() doesn't work 
import os.path  # Used for determining if file path is valid

app = Flask(__name__)   # template_folder="templates", static_folder="static"

# app.route("/<path>")
@app.route("/<path>") # route() tells Flask what URL should trigger function
def respond(path):  # Searching from root or having the <path> variable
    log.info("\n--- Received request ----")
    log.info("Request URL was {}\n***\n".format(request.url))

    response = None
    log.info("PORT is " + port)
    log.info("PATH IS " + path)

    # TODO: Where do templates/ directory and the error files in it go upon submission
    # TODO: Don't limit this just to HTML, move the path.exists() up here to bigger if condition
    if path.endswith('.html') or path.endswith('.css') or path.endswith('.txt'):
        if '~' in path or '//' in path or '..' in path:
            abort(403)
            # alternatively(?): return redirect(url_for('page_forbidden'))
        elif not os.path.exists(path):
            abort(404)
        else:
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200     # Transmit content of file with a 200 OK HTTP code
    else:
        return "That request is not handled", 401   # 401 was Not Impelemented from proj1

    # return flask response object?

@app.route("/<path>/<subpath>") # route() tells Flask what URL should trigger function
def respond_subpath(path, subpath):  # Searching from root or having the <path> variable
    path = path + "/" + subpath

    log.info("PATH IS " + path)

    if path.endswith('.html') or path.endswith('.css') or path.endswith('.txt'):
        if '~' in path or '//' in path or '..' in path:
            abort(403)
            # alternatively(?): return redirect(url_for('page_forbidden'))
        elif not os.path.exists(path):
            abort(404)
        else:
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200     # Transmit content of file with a 200 OK HTTP code
    else:
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

