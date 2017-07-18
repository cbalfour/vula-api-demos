# Vula/Sakai API Demos

[Vula](https://vula.uct.ac.za) is the [University of Cape
Town](http://www.uct.ac.za)'s instance of the
[Sakai](https://www.sakaiproject.org) Learning Management System (LMS).

This project will (hopefully, eventually) contain example code that
demonstrates the basics of using the various Sakai API's to interact
with Vula.

Most of the code is/will probably be written in
[Python](https://www.python.org) version 3 using the
[Flask](http://flask.pocoo.org/) framework where necessary.

## APIs

Sakai provides a number of APIs.

### General

* LTI
* Direct
* Sakai-WS: REST and SOAP

### Authentication

* OAuth 1.0
* ADFS
* CAS

### File Management

* WebDAV

## Considerations

The API/s you choose will depend on a number of factors including:

* Integration: How closely does the application need to integrate into
  the Sakai web interface? Do you want it to appear as just 
  another function within the Sakai web interface, or will it be a 
  completely separate interface? 
  
* Data: What datastores does your application need access to? Does it
  rely on data stored in Sakai or does it use its own data? 

* Authentication and authorization: Do you want to be responsible for
  authenticating to Sakai or would you prefer to defer this to Sakai
  and receive an already authenticated session to work with? 





