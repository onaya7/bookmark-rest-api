#   Bookmark management system API

This is a Bookmark managment system built with Flask API

## Overview
A bookmark API is a web-based application programming interface that allows users to manage their bookmarks. This API provides a set of endpoints that enable users to perform CRUD (Create, Read, Update, Delete) operations on their bookmarks.With a bookmark API, users can create, store, retrieve, update, and delete bookmarks.
The bookmark API can be used in a variety of applications, such as web browsers, mobile apps, or bookmark manager tools. For example, a web browser can use the bookmark API to sync bookmarks across multiple devices, while a bookmark manager tool can use the API to provide a unified interface for managing bookmarks from different sources.

## Security and privacy
Security is an important consideration for a bookmark API, as it involves sensitive user data. This API support authentication and authorization mechanisms to ensure that only authorized users can access and modify their bookmarks. Additionally, the API should use HTTPS encryption to secure the data in transit.

![Screenshot (48)](https://user-images.githubusercontent.com/63925047/232069081-c2fb33b2-e857-4325-9500-18bc7627d786.png)
![Screenshot (46)](https://user-images.githubusercontent.com/63925047/232069067-ddbbeec3-3db7-4f22-8487-df34d0974438.png)
![Screenshot (45)](https://user-images.githubusercontent.com/63925047/232069056-f811d576-bb8d-427d-9404-4e825c048562.png)
![Screenshot (47)](https://user-images.githubusercontent.com/63925047/232069076-d3c706f4-5511-44db-b6ee-5bc8b5416817.png)
![Screenshot (106)](https://user-images.githubusercontent.com/63925047/210275145-caad10ad-913d-448e-9927-9dfcaeb09673.png)


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
FLASK_APP=run
FLASK_ENV=development
FLASK_DEBUG=TRUE


```

Then run:

```
flask run

```
### Testing the server
Once started, you can navigate to 
http://127.0.0.1:5000/bookmark-api.json to view the Swagger Resource Listing.
This tells you that the server is up and ready to demonstrate Swagger.
### Using the UI
There is an HTML5-based API tool bundled in this sample--you can view it it at [http://localhost:5000](http://localhost:8080). This lets you inspect the API using an interactive UI.  You can access the source of this code from [here](https://github.com/swagger-api/swagger-ui)
​
## Resources
-   Flasgger documentation
https://github.com/flasgger/flasgger

