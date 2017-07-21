# Sakai/Vula LTI Application Demo

A simple LTI application to demonstrate the use of LTI with Sakai/Vula.

## Assumptions

This document assumes that you are familiar with the following components used in this project:

* [Python](https://python.org)
* [Python virtual environments](https://virtualenv.pypa.io/en/stable/)
* [Flask](http://flask.pocoo.org)
* [Sakai](https://www.sakaiproject.org/) and particular the [University of Cape Town](http://www.uct.ac.za) [vula](https://vula.uct.ac.za) implementation

A basic familiarity with [Learning Tools Interoperability](https://www.imsglobal.org/activity/learning-tools-interoperability) would be helpful.

## Dependencies 

* [Flask](http://flask.pocoo.org). 
* [PyLTI](http://pylti.readthedocs.io)
* [pyOpenSSL](https://pyopenssl.org/en/stable/)

These dependencies can be installed using ``pip`` and the included ``requirements.txt`` file.

As PyLTI does not support Python 3, Python 2 is required. 

## Installation

It is recommended that this demo is setup in a python virtual environment.

```
virtualenv -p python venv
. venv/bin/activate
pip install -r requirements.txt
```


Start up the application server listening on port 5443 on all interfaces.
```
python app.py
```

## SSL Configuration

Ideally the LTI application should appear inline in a Sakai rather than in a separate window, tab or popup. 

For security reasons, browsers no longer permit insecure content to be inlined into secure sites. It is therefore necessary for LTI applications/consumers to use HTTPS/SSL when integrated with HTTPS/SSL enabled LMS servers. As UCT's Sakai/vula system uses SSL/HTTPS this demo needs to use HTTPS to appear inline. 

This demo uses Flask's SSL functionality together with a self-signed certificate. Before, the LTI application will work you need to convince your browser to trust this certificate. With the demo application server started, visit ``/trust_cert``. The untrusted certificate warning should be displayed. Most browsers include a (often hidden) option on this page to ignore the warning and temporarily trust the certificate. Follow your browsers process to trust the certificate. Once trusted the LTI application will be able to appear inline in the Sakai environment.

Use the ``setup_cert.sh`` script to create a self-signed certificate and key pair as follows:
```
./setup_cert.sh <hostname>
```
Where ``<hostname>`` is the name of the server running the LTI application as used in the _Launch URL_ configuration of the _Sakai Setup_  below. Enter a passphrase when prompted. This passphrase while required to setup the certificate is stripped from the final certificate so can be any arbitrary value.

**Note:**

In production:
* you will need to use a certificate trusted by your customers' browsers - such as one from [letsencrypt.org](https://letsencrypt.org). 
* you should probably not use Flask's web server directly. Intergrate it into a 'proper' web server such as [Apache](http://apache.org) using [WSGI](http://wsgi.readthedocs.io/en/latest/what.html).

As the full URL - including the http:// or https:// - is used as part of the LTI verification process it is important that both Sakai and the application use the same protocol. If Sakai is configured to access the application over HTTPS via a reverse proxy which communicates with the application over HTTP in the backend the LTI verification will fail and you will get an OAuth error. 

## Application Configuration

The LTI consumer key and secret are configured in ``config.py`` as follows: 
```
PYLTI_CONFIG = {
    'consumers': {
        'hello': {
            'secret': 'hello_secret1970'
        },
    }
}
```
These values must match the _Launch Key_ and _Launch Secret_ in the _Sakai/Vula Setup_ configuration below.

## Sakai/Vula Setup

These instructions assume the customised vula site setup. Additional configuration will probably be required in a default Sakai installation.

To perform this setup, you need to be a privileges user - owner, support, lecturer - of the Sakai site.

Define the application as follows:

1. Click _Site Setup_ from the menu on the left.
2. Click the _External Tools_ tab at the top of the Site Setup page.
3. Click the _Install LTI 1.1 Tool_ link on the right side of the External Tools page.
4. Fill in the fields to configure your application. Take particular note of the following:
* **Tool Title**: _Hello LTI Demo_. The name of the app which appears in the list of available external tools.
* **Button Text**: _Hello Demo_. The name that appears on the menu button.
* **Launch URL**: _https://foo.example.com:5443/setup_. The URL of this app. Note that if you want your application to open in the iframe in the vula interface it must be an https:// URL using a certificate trusted by your web browser. This is because most (all?) browsers now refuse to inline in-secure sources into secure pages. If you specify a http:// URL vula will, by default, open it in a separate tab. If you need to use the http but don't want a separate tab you can select "Always launch in Popup" in the Launch in Popup section (though again, your browser may block popups by default so this might not work)
* **Launch Key**: _hello_. The LTI consumer key. This must match the consumer key defined in the ``PYLTI_CONFIG`` dictionary in ``config.py``.
* **Launch Secret**: _hellosecret1970_. The LTI consumer secret. This must match the consumer secret defined in the ``PYLTI_CONFIG`` dictionary in ``config.py``.
* **Privacy Settings**. Check the _"Send User Names to External Tool"_ and _"Send Email Addresses to External Tool"_ checkboxes
* **Services**: Check _"Provide Roster to External Tool"_ checkbox.
5. Click the _Save_ button

Activate the application as follows:

1. Click _Site Setup_.
2. Click the _Manage Tools_ tab.
3. Expand _Plugin Tools_ at the bottom of the page and check the checkbox next to the tool you defined above.
3. Click the _Continue_ button. The tool should appear on the menu on the left. 

To change the order of the tools use the _Organize Tools_ tab in _Site Setup_.

## Usage

Once the application is configured in Sakai, the server is started and the self signed certificate is trusted click on the _Hello Demo_ button on the Sakai toolbar. 

If everything is correctly setup, Sakai will establish a LTI connection to the application via a HTTP POST the _/setup_ page. 

If the LTI verification succeeds a verified session is established and the application is automatically redirected to the _/hello_ page. If the LTI session is still valid, this page will display some information provided to the application by Sakai available via the _lti_ object and _session_ dictionary.

Examine the source code of ``app.py`` to see how LTI is configured in the Flask endpoints.
