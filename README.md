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

* **Integration**: How closely does the application need to integrate into
  the Sakai web interface? Do you want it to appear as just 
  another function within the Sakai web interface, or will it be a 
  completely separate interface? 
  
* **Data**: What datastores does your application need access to? Does it
  rely on data stored in Sakai or does it use its own data? 

* **Authentication and authorization**: Do you want to be responsible for
  authenticating to Sakai or would you prefer to defer this to Sakai
  and receive an already authenticated session to work with? 

## Recommendations

* Mobile: Direct REST API, ideally with OAuth 1.0 authentication [*]. 

* Web
- Javascript/ajax front-end: Direct REST API ideally with OAuth
  1.0 authentication. [*] 
- Integrated into Sakai web interface but only requiring
  limited personal information from: LTI
- Integrated into Sakai web interface requiring
  extensive interaction with the Sakai backend: Sakai-WS REST API


## LTI

Learning Tools Interoperability.

Standard for writing platform-agnostic tools. In theory, an LTI
application written for Sakai should also work with other LTI-compliant
systems such as Moodle.

It, however, provides very limited access to the Sakai backend and
is therefore only useful for largely independent applications which 
require very loose integration.

LTI provides: 
* A trust mechanism between Sakai and your application
* Integration into the web interface
* An authenticated and authorized session
* Some basic information about the user
* The ability to pass back a score to the gradebook. 

### Advantages
* Easy to use 
* Platform-agnostic

### Disadvantages
* Very limited access 

### Example Applications

* A Simple grant application. LTI is used to authenticate the user and
  provide basic information for pre-populating some fields of a web form
  on the 3rd party system. The 3rd party system processes the form,
  stores the results, determines and communicates the outcome to the
  user.

* A simple marking system. LTI is used to authenticate the user to the
  3rd party system. The 3rd party system presents some questions via a
  web form which the user answers and submits back to the 3rd party
  system. The 3rd party system evaluates the answers to the questions
  and returns a single score to an appropriate entry in the gradebook.
  It is not suitable for a more complex marking system since it can only
  return a single score to a single gradebook entry.

## Direct API

This is a REST HTTP API that can access the majority of the Sakai's 
functionality. 

Data is returned as JSON or XML.

It is best for stand-alone applications which require only require no 
integration into the Sakai web interface.

An authenticated session can be obtained via web login, via the
appropriate direct API endpoint or via  OAuth 1.0.

### Endpoints
[https://vula.uct.ac.za/direct](https://vula.uct.ac.za/direct) This 
includes basic interface documentation for all endpoints. 


### Example Applications

* A mobile application. 
* Ajax web applications. 
* Scripts. 

## Sakai-WS

This is an older API which provides both a SOAP and REST interface.
It's primary advantage is that it can be used via the Linktool 
functionality. 

### Endpoints
* SOAP: [https://vula.uct.ac.za/sakai-ws/soap](https://vula.uct.ac.za/sakai-ws). This includes basic interface documentation for all endpoints.
* REST: A list of REST endpoints is provided at the end of the above
  SOAP endpoint documentation. 



It can be used with the Linktool.







