#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for
from pylti.flask import lti, LTINotInSessionException
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)
app.config.from_object('config')

def error(exception=None):
    return render_template("error.html", exception=exception)

# Verify the LTI credentials and setup the session
@app.route('/setup', methods=['POST', 'GET'])
@lti(request='initial', error=error, app=app)
def setup(lti=lti):
    return redirect(url_for('hello'))


@app.route('/hello', methods=['GET'])
@lti(request='session', error=error, app=app)
def hello(lti=lti):
    return render_template('hello.html', lti=lti, session=session)

# A non-LTI endpoint to use to test whether the browser trusts our
# certificate. 
@app.route('/trust_cert', methods=['GET'])
def trust_cert():
    return 'If you see this your browser hopefully trusts our cert'

if __name__ == '__main__':

    context = ('ssl/server.crt', 'ssl/server.key')
#    app.run(host="0.0.0.0", port=5080, debug=True)
    app.run(host="0.0.0.0", port=5443, ssl_context=context,
            threaded=True,  debug=True)

