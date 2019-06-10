A very simple Sakai-WS (web services) interface demo.

Setup the virtual environment.

virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt

Setup the SSL certificates in the ssl/ sub-directory

Start the application server. It is configured to run on port 5443
using the SSL certificates you put in ssl/ subdirectory.

Vula setup

Get the vula admins to add the LinkTool to vula site. 
Rename the linktool to something useful.
Point the linktool to this application landing page. Something 
like: https://yoursite.co.za/hello
If all goes well, you should see the Hello, World page which 
includes a list of the session variables gathered from vula via the
linktool.


