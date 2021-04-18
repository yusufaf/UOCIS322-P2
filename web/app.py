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

import config    # Configure from .ini files and command line
import sys      # Used for printing because regular print() doesn't work 
import os.path  # Used for determining if file path is valid

app = Flask(__name__)   # template_folder="templates", static_folder="static"
PORT = None

# app.route("/<path>")
@app.route("/<path>") # route() tells Flask what URL should trigger function
def respond(path):  # Searching from root or having the <path> variable
    log.info("\n--- Received request ----")
    log.info("Request URL was {}\n***\n".format(request.url))

    response = None

    # log.info("PORT is " + PORT)
    log.info("PATH IS " + path)

    # TODO: Where do templates/ directory and the error files in it go upon submission
    # TODO: Don't limit this just to HTML, move the path.exists() up here to bigger if condition
    if path.endswith('.html') or path.endswith('.css') or path.endswith('.txt'):
        if '~' in path or '//' in path or '..' in path:
            abort(403)
            # alternatively(?): return redirect(url_for('page_forbidden'))

            # response = make_response(render_template("../403.html"),403)
        elif not os.path.exists(path):
            abort(404)
            # response = make_response(render_template("../404.html"),404)
        else:
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200
    else:
        return "That request is not handled", 401   # 401 was Not Impelemented from proj1

    # return flask response object?


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403     # Wrap these in make_response() or no (?)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6500)
    # options = config.configuration()
    # PORT = options.PORT

    # Supposed to read in PORT from credentials.ini?
