#!/usr/bin/env python

# Sakai web services demo code
# CTB Tue May 15 18:48:47 SAST 2018

from flask import Flask, request, render_template, session
from flask.ext.session import Session
from zeep import Client

app = Flask(__name__)
app.secret_key = 'kdflgjdfiogn odfaudaodf'
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

@app.route('/hello', methods=['GET'])
def hello():
    url = 'https://vula.uct.ac.za/sakai-ws'
    q = request.query_string
    wsdl = 'https://vula.uct.ac.za/sakai-ws/soap/signing?wsdl'
    client = Client(wsdl=wsdl)
    testsign = client.service.testsign(data=request.query_string)
    if testsign != 'true':
        return 'Please re-authenticate.'

    for i in request.args.keys():
        session[i] = request.args[i]

    print (session.keys())
    return render_template('hello.html')


if __name__ == '__main__':
    context = ('ssl/server.crt', 'ssl/server.key')
    app.debug = True
    app.run(host='0.0.0.0', port=5443, ssl_context=context, threaded=True, debug=True)
