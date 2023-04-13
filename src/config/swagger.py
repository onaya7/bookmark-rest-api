template = {
  "swagger": "2.0",
  "info": {
    "title": "Bookmark API",
    "description": "Bookmark API for my data",
    "contact": {
      "responsibleOrganization": "Dev_onaya",
      "responsibleDeveloper": "Samuel Ayano",
      "email": "samuelayano7@gmail.com",
      "url": "https://www.linkedin.com/in/samuel-ayano-1336bb247/",
    },
    "termsOfService": "http://me.com/terms",
    "version": "1.0"
  },
  "host": "localhost:5000",  # overrides localhost:500
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
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}