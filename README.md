# find-it-backend
[![Build Status](https://travis-ci.org/ongebo/find-it-backend.svg?branch=master)](https://travis-ci.org/ongebo/find-it-backend)
[![Maintainability](https://api.codeclimate.com/v1/badges/799d0b624fbf6364f8e9/maintainability)](https://codeclimate.com/github/ongebo/find-it-backend/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/ongebo/find-it-backend/badge.svg?branch=master)](https://coveralls.io/github/ongebo/find-it-backend?branch=master)

This is a Python/Flask backend designed for an Android app to find/report lost and found items. It is staged on Heroku at this [base url](https://findit-backend-staging.herokuapp.com). Key features include:
- Authentication (Signup and Login)
- Reporting lost and found items
- Viewing lost and found items
- Updating/Deleting lost and found items

## Environment Setup
Follow these instructions to create a local development environment:
### 1.  clone and checkout this repository with:
- `git clone https://github.com/ongebo/find-it-backend.git`
- `cd find-it-backend`

### 2.  set up and activate a virtual environment:
- `python3 -venv env`
- `. env/bin/activate`

### 3.  ensure pip is up-to-date and install all dependencies:
- `pip install --upgrade pip`
- `pip install -r requirements`

### 4.  setup PostgreSQL:
- Make sure a [PostgresSQL](https://www.postgresql.org/) server is running locally
- Create two PostgresSQL databases: a main database(e.g `find_it`) and a test database (e.g `find_it_test`)

### 5.  set up the following environment variables:
- `DATABASE_URL`: The main database (e.g. `postgres://username:password@localhost:5432/find_it`)
- `TEST_DATABASE_URL`: The test database (e.g. `postgres://username:password@localhost:5432/find_it_test`)
- `JWT_SECRET_KEY`: A long and random string
-  `UPLOAD_FOLDER`: A directory on the local system with write permissions (e.g. `/home/folder/uploads`)

## Running
When running the application for the first time, make sure both main and test database tables are created using the `db_setup.py` script:

- Run `python db_setup.py` to create tables in the main database
- Run `python db_setup.py testdb` to create tables in the test database

Run the application with `python run.py`. To enable debug mode, set the `FLASK_ENV` environment variable to `development` before running.

## Testing
- Run tests and generate a coverage report with `pytest --cov=app`.

## Endpoints
With the application running, test the following endpoints using [Postman](https://www.getpostman.com/).
### Registration:
`POST /users`

```javascript
{
  "username": "John Doe",
  "phone_number": "+1-343-879124",
  "email": "johndoe@gmail.com",
  "password": "J0hnDoe"
}
```

### Login:
`POST /login`

```javascript
{
  "emai": "johndoe@gmail.com",
  "password": "J0hnDoe"
}
```

### Upload an Image of a Lost and Found Item:
`POST /items/images`

Specify a .png, .jpg, or .jpeg image file less than 5 MBs for upload. The API returns a URL to the uploaded image which can be used as `image_url` when reporting the lost and found item.

### Report Lost and Found Item:
`POST /items`

```javascript
{
  "item_name": "iPhone",
  "description": "Found misplaced at the cafeteria.",
  "image_url": "http://somehost.com/iphone.png"
}
```

### Fetch all Lost and Found Items:
`GET /items`

Sample response:
```javascript
{
  "items": [
    {
      "description": "Found misplaced at the cafeteria.",
      "id": 1,
      "image_url": "http://image.server.com/some-image.png",
      "item_name": "Calculator",
      "report_date": "Fri, 30 Aug 2019 17:27:37 GMT",
      "reported_by": "John Doe"
    },
    {
      "description": "Inspiron model of 2018.",
      "id": 2,
      "image_url": "http://image.server.com/some-image.png",
      "item_name": "DELL laptop",
      "report_date": "Fri, 30 Aug 2019 17:27:37 GMT",
      "reported_by": "Jane Doe"
    },
    {
      "description": "Made by Apple.",
      "id": 3,
      "image_url": "http://image.server.com/some-image.png",
      "item_name": "Wireless AirPods",
      "report_date": "Fri, 30 Aug 2019 17:27:37 GMT",
      "reported_by": "Anastatia Steele"
    },
    {
      "description": "Yellow Hoodie labelled Magic.",
      "id": 4,
      "image_url": "http://image.server.com/some-image.png",
      "item_name": "Jacket",
      "report_date": "Fri, 30 Aug 2019 17:38:29 GMT",
      "reported_by": "Bjorn Ironside"
    },
    {
      "description": "Green bottle with a black cover.",
      "id": 5,
      "image_url": "http://image.server.com/some-image.png",
      "item_name": "Bottle",
      "report_date": "Fri, 30 Aug 2019 17:38:29 GMT",
      "reported_by": "Little Finger"
    }
  ]
}
```

### Fetch Specific Lost and Found Item:
`GET /items/1`

```javascript
{
  "description": "Found misplaced at the cafeteria.",
  "id": 1,
  "image_url": "http://image.server.com/some-image.png",
  "item_name": "Calculator",
  "report_date": "Fri, 30 Aug 2019 17:27:37 GMT",
  "reported_by": "John Doe"
}
```

### Fetch Specific Lost and Found Item:
`PUT /items/1`

```javascript
{
  "item_name": "Calculator",
  "description": "Found misplaced at the cafeteria, model FX 991 MS",
  "image_url": "http://image.server.com/some-image.png",
}
```

### Delete Specific Lost and Found Item:
`DELETE /items/1`
