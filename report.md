<!-- ## I. Definition
## II. Next def

### Project Overview

An [estimated 2 trillion photos](http://ben-evans.com/benedictevans/2015/8/19/how-many-pictures)

![AltraNikeLogo](images/AltraNikeLogo.png) -->

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

|     DELETE   |        [hostname]/img/api/v1.0/imgs/[img_id]   | Delete an existing image     |

Results from





## 2. Image Inference
|  HTTP Method |                           URI                    |                                  Action                                      |
|--------------|--------------------------------------------------|------------------------------------------------------------------------------|
|     PUT      |     [hostname]/img/api/v1.0/inference/[img_id]   |runs inference on an existing image and adds results to image file store entry|

## 3. Image Inference
|  HTTP Method |                           URI                    |                                   Action                                 |
|--------------|--------------------------------------------------|--------------------------------------------------------------------------|
|     PUT      |     [hostname]/img/api/v1.0/resize/[img_id]      |measures size of existing image and adds results to image file store entry|

curl -u ReturnPath:python -X PUT -H "Content-Type: application/json" -d '{"id":3}' http://127.0.0.1:5000/img/api/v1.0/inference/3

<pre class="embedcurl">curl -u ReturnPath:python -X PUT -i -H "Content-Type: application/json" -d '{"id":2}' http://127.0.0.1:5000/img/api/v1.0/inference/2</pre>


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

REST


## Improvements:
- IAM roles for AWS http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
- better type checking for images

<script src="https://www.embedcurl.com/embedcurl.min.js" async></script>
