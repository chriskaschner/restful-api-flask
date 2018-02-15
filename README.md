This project has been updated for Python 3

# Requirements:
This project requires**Python 3.6**and[Pipenv](https://github.com/pypa/pipenv)to manage virtual environments and package dependencies.

### Building a RESTful API with Flask for image recognition

In a [previous project](chriskaschner.com/retraining), I created a Convolutional Neural Network (CNN) that can identify brand logos (specifically Nike and Altra) in untagged/ unlabeled photos from a social media feed.  The model I used implemented a [previously trained](https://github.com/tensorflow/models/tree/master/inception) network and [transfer learning](https://en.wikipedia.org/wiki/Inductive_transfer).

For this project I wanted to build a REST API that allowed me to send requests to that neural network and return a response in JSON.

The original incarnation of this project was developed as a solution for a [GapJumpers Challenge](https://www.gapjumpers.me/questions/return-path/qs-323/)

The challenge specifies the following for a successful submission:

- Write a simple Rest API with PHP, Node.js, Ruby, Python or Go.
- Your API must have:
	- at least three endpoints
	- all endpoints must be linked in some way
- Pay careful attention to REST best practices
- Describe the application in detail in a design document including why you chose the approach you did.
- include tests that validate success.

### Deliverables
- Using Python and Flask, I created [this website](https://chriskaschner.github.io/restful-api-flask/) that allows for retrieval of data from my endpoints.  The 3 endpoints are described in detail in the API Documentation section.
- In order to share my application and provide links where it can be tested - links and curl embeds are included throughout that document that allow for interacting with the API directly.  The API is currently live at [http://10la.pythonanywhere.com/img/api/v1.0/images](http://10la.pythonanywhere.com/img/api/v1.0/images) and all references to a [hostname] in this documentation refers to `http://10la.pythonanywhere.com`.  The [application](https://github.com/chriskaschner/restful-api-flask/blob/master/app.py), it's [unit tests](https://github.com/chriskaschner/restful-api-flask/blob/master/test_app.py), and all supporting documentation can be found at the [project's GitHub](https://github.com/chriskaschner/restful-api-flask).  
- [This website](https://chriskaschner.github.io/restful-api-flask/) represents the design document.  In particular the sections dedicated to the REST Architecture and API Documentation discuss the design process in detail.
- Unit tests, including those that validate success, are available in a number of ways.  Basic functionality can be verified by executing each curl command in order it appears in the the API Documentation.  A copy of the output of the unit test application is included in the Unit Tests section.  Finally, the [test application](https://github.com/chriskaschner/restful-api-flask/blob/master/test_app.py) can be downloaded from GitHub and run locally.
