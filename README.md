#   Bookmark management system API

This is a Bookmark managment system built with Flask Restful API

![Screenshot (107)](https://user-images.githubusercontent.com/63925047/210275144-ea559540-ac31-4c0c-9058-1b54d1f5798a.png)
![Screenshot (106)](https://user-images.githubusercontent.com/63925047/210275145-caad10ad-913d-448e-9927-9dfcaeb09673.png)
![Screenshot (105)](https://user-images.githubusercontent.com/63925047/210275146-19d4732d-284a-47a6-a28d-9be8c86d0976.png)

## Project setup
- Flask Api Folder structure
- Application Factory, .flaskenv
- Flask API Blueprints
- Database and Models setup
- HTTP Status codes
- User Registation
- User Login
- Route protection
- Refreshing a token

## Bookmark Section
- Create and Retrieve records
- Pagination for records
- Retrive a single bookmark record
- Updating a bookmark
- Deleting a bookmark 
- User link click tracking
- Error handling 
- Get link stats
- Swagger Documentation

## How to run this application locally

To install all the packages, run:

```
pip3 install -r requirements.txt

```

create a .flaskenv and include:

```
FLASK_APP=src
FLASK_ENV=development
FLASK_DEBUG=TRUE


```

Then run:

```
flask run

```
### Testing the server
Once started, you can navigate to 
http://127.0.0.1:5000/apispec.json to view the Swagger Resource Listing.
This tells you that the server is up and ready to demonstrate Swagger.
### Using the UI
There is an HTML5-based API tool bundled in this sample--you can view it it at [http://localhost:5000](http://localhost:8080). This lets you inspect the API using an interactive UI.  You can access the source of this code from [here](https://github.com/swagger-api/swagger-ui)
​
## Resources
-   Flasgger documentation
https://github.com/flasgger/flasgger

