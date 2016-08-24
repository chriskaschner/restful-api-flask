<!-- ## I. Definition
## II. Next def

### Project Overview

An [estimated 2 trillion photos](http://ben-evans.com/benedictevans/2015/8/19/how-many-pictures)

![AltraNikeLogo](images/AltraNikeLogo.png) -->

## REST Architecture

Representational state transfer (REST) originally specified in the [5th chapter](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) of Roy Fielding's PhD thesis "Architectural Styles and
the Design of Network-based Software Architectures" which specifies 6 constraints for the REST architecture.

1. Client-Server
1. Stateless
1. Cache
1. Uniform Interface - including HATEOAS (Hypermedia As The Engine Of Application State)
https://en.wikipedia.org/wiki/HATEOAS
1. Layered System
1. Code-On-Demand

REST defines an architectural style used in web development.  Because it defined an architecture and not a specification, there is room for interpretation.

###### stuff I do that makes sense
1. GET requests get data
1. PUT requests update existing data
1. POST requests create new data
1. DELETE requests delete data

###### Versioning
There's some argument about *where* to place the version information for your API, but not *if* you should version it.  I place versioning info in the URL.  The other alternative is in the header.

###### JSON
It's ubiquitous.  It's human readable.  It's easy to work with.

### References
http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api


Versioning

Your API must have:
- at least three endpoints
- all endpoints must be linked in some way

- A single page website that allows for retrieval of data from your endpoints
-
- Share your application and provide a link where it can be tested
- Design Document
	- Please pay careful attention to Rest best practices and describe the application in detail in a design document including why you chose the approach you did.
- Unit Tests
	- Unit tests are included in the file "test_app.py"
	-  Also, include tests that validate success.

## 3 endpoints
### 1. Images File Store
|  HTTP Method |                           URI                  |             Action           |
|--------------|------------------------------------------------|------------------------------|
|     GET      |        [hostname]/img/api/v1.0/imgs            | Retrieve list of images      |  
|     POST     |        [hostname]/img/api/v1.0/imgs            | Create new image             |
|     GET      |        [hostname]/img/api/v1.0/imgs/[img_id]   | Retrieve an individual image |  
|     PUT      |        [hostname]/img/api/v1.0/imgs/[img_id]   | Update an existing image     |
|     DELETE   |        [hostname]/img/api/v1.0/imgs/[img_id]   | Delete an existing image     |


#### GET [hostname]/img/api/v1.0/imgs
<pre class="embedcurl">curl -i http://chriskaschner.pythonanywhere.com/img/api/v1.0/images</pre>

##### Results:
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 502
Server: Werkzeug/0.9.6 Python/2.7.12
Date: Wed, 24 Aug 2016 22:06:07 GMT

{
  "images": [
    {
      "resize": false,
      "results": "",
      "size": "",
      "title": "Nikes",
      "uri": "http://127.0.0.1:5000/img/api/v1.0/images/1",
      "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/nike.jpg"
    },
    {
      "resize": false,
      "results": "",
      "size": "",
      "title": "Altra",
      "uri": "http://127.0.0.1:5000/img/api/v1.0/images/2",
      "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/altra.jpg"
    }
  ]
}
```

#### POST [hostname]/img/api/v1.0/imgs
<pre class="embedcurl">curl -u ReturnPath:python -i -H "Content-Type: application/json" -X POST -d '{"url":"http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"}' http://127.0.0.1:5000/img/api/v1.0/images</pre>

##### Results:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 233
Server: Werkzeug/0.9.6 Python/2.7.12
Date: Wed, 24 Aug 2016 22:13:57 GMT

{
  "image": {
    "resize": false,
    "results": "",
    "size": "",
    "title": "",
    "uri": "http://127.0.0.1:5000/img/api/v1.0/images/3",
    "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"
  }
```

#### GET [hostname]/img/api/v1.0/imgs/[img_id]

<pre class="embedcurl">curl -u ReturnPath:python -i http://127.0.0.1:5000/img/api/v1.0/image/3</pre>


##### Results:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 186
Server: Werkzeug/0.9.6 Python/2.7.12
Date: Wed, 24 Aug 2016 22:19:02 GMT

{
  "img": {
    "id": 3,
    "resize": false,
    "results": "",
    "size": "",
    "title": "",
    "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"
  }
```



            |
#### PUT [hostname]/img/api/v1.0/imgs/[img_id]

<pre class="embedcurl">curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT -d '{"title":"C-ron-ron"}' http://127.0.0.1:5000/img/api/v1.0/images/3</pre>

##### Results:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 195
Server: Werkzeug/0.9.6 Python/2.7.12
Date: Wed, 24 Aug 2016 22:43:20 GMT

{
  "img": {
    "id": 3,
    "resize": false,
    "results": "",
    "size": "",
    "title": "C-ron-ron",
    "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"
  }
```

#### DELETE [hostname]/img/api/v1.0/imgs/[img_id]

<pre class="embedcurl">curl -u ReturnPath:python -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/img/api/v1.0/images/3</pre>

##### Results:

```
	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 20
	Server: Werkzeug/0.9.6 Python/2.7.12
	Date: Wed, 24 Aug 2016 23:13:36 GMT

	{
	  "result": true
	}
```

## 2. Image Inference

#### PUT [hostname]/img/api/v1.0/resize/[img_id]

<pre class="embedcurl">curl -u ReturnPath:python -X PUT -i -H "Content-Type: application/json" -d '{"id":2}' http://127.0.0.1:5000/img/api/v1.0/inference/2</pre>

##### Results:
```
	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 415
	Server: Werkzeug/0.9.6 Python/2.7.12
	Date: Wed, 24 Aug 2016 22:47:30 GMT

	{
	  "img": {
	    "id": 2,
	    "resize": false,
	    "results": {
	      "results_name_1": "neither",
	      "results_name_2": "altra",
	      "results_name_3": "nike",
	      "results_score_1": "\"0.7680\"",
	      "results_score_2": "\"0.2004\"",
	      "results_score_3": "\"0.0316\""
	    },
	    "size": "",
	    "title": "Altra",
	    "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/altra.jpg"
	  }
	}
```

## 3. Image Resize

<pre class="embedcurl">curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/img/api/v1.0/resize/3</pre>

##### Results:
```
	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 235
	Server: Werkzeug/0.9.6 Python/2.7.12
	Date: Wed, 24 Aug 2016 23:18:53 GMT

	{
	  "img": {
	    "id": 2,
	    "resize": false,
	    "results": "",
	    "size": {
	      "height": 480,
	      "width": 480
	    },
	    "title": "Altra",
	    "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/altra.jpg"
	  }
	}
```
## Improvements:
- IAM roles for AWS http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
- better type checking for images

<script src="https://www.embedcurl.com/embedcurl.min.js" async></script>
