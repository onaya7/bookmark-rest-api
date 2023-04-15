template = {
  "swagger": "2.0",
  "info": {
    "title": "Bookmark API",
    "description": "The bookmark API is a web-based application programming interface that allows users to manage their bookmarks. This API provides a set of endpoints that enable users to perform CRUD (Create, Read, Update, Delete) operations on their bookmarks.",
    "contact": {
      "responsibleOrganization": "Dev_onaya",
      "responsibleDeveloper": "Samuel Ayano",
      "email": "samuelayano7@gmail.com",
      "url": "https://www.linkedin.com/in/samuel-ayano-1336bb247/",
    },
    "termsOfService": "http://me.com/terms",
    "version": "1.0"
  },
  "host": "https://bookmark-api-3nfy.onrender.com",  # overrides localhost:500
  "basePath": "/api/v1",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
   "securityDefinitions": {
            "JWTAuth": {
            "type": "apiKey",
            "scheme": "bearer",
            "name": "Authorization",
            "bearerFormat": "JWT",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        },
        
    },
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'bookmark-api',
            "route": '/bookmark-api.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}