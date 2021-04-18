"""
Yusuf Afzal's Flask API.
"""

from flask import Flask, request, render_template, Response, make_response
                # request has data like the requested URL
                # render_template provides for the response

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

import sys      # Used for trying to print 
import os.path  # Used for determining if file path is valid

app = Flask(__name__)

STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"


# app.route("/<path>")
# if path.endswith('.html'):
# if os.path.exists(path)
@app.route("/<path>") # route() tells Flask what URL should trigger function
def respond(path):
    log.info("\n--- Received request ----")
    log.info("Request URL was {}\n***\n".format(request.url))

    response = None

    # TODO: Figure out which directory these 403 and 404.html files are; in parent of web folder?
    if path.endswith('.html'):
        if '~' in path or '//' in path or '..' in path:
            abort(403)
            # response = make_response(render_template("../403.html"),403)
        elif not os.path.exists(path):
            abort(404)
            # response = make_response(render_template("../404.html"),404)
        else:
            with open(path, 'r+') as f:
                content = f.read()
            return content, 200

    # return flask response object?


@app.errorhandler(403)
def page_forbidden(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6500)
