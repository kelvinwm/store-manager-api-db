[![Coverage Status](https://coveralls.io/repos/github/kelvinwm/store-manager-api-db/badge.svg?branch=travis-config)](https://coveralls.io/github/kelvinwm/store-manager-api-db?branch=travis-config)
[![Build Status](https://travis-ci.org/kelvinwm/store-manager-api-db.svg?branch=heroku-config)](https://travis-ci.org/kelvinwm/store-manager-api-db)
[![Maintainability](https://api.codeclimate.com/v1/badges/a763257e90829b1e6e99/maintainability)](https://codeclimate.com/github/kelvinwm/store-manager-api-db/maintainability)

## store-manager-api

Store Manager is a web application that helps store owners manage sales and product inventory
records. This application is meant for use in a single store

## Getting Started

Instructions on how to run on your local machine for development and testing purposes. 

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
https://github.com/kelvinwm/store-manager-api-db
```
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Run the development server

```
$ python run.py
```

5. Navigate to [http://localhost:5000](http://localhost:5000)

## Endpoints
Here is a list of all endpoints for store manager API

Endpoint | Functionality 
------------ | -------------
1.POST /api/v2/auth/signup |	Register a user
POST /api/v2/auth/login	| Log in user
POST /api/v2/auth/logout	| Log out user
PUT /api/v2/users/id |	Update user role
GET /api/v2/users	| get all registered users
POST /api/v2/category	| Add a category
GET /api/v2/category	| Get all categories
PUT /api/v2/category/id |	Update a category
DELETE /api/v2/category/id | Delete a category
POST /api/v2/products	| Add a product
POST /api/v2/sales	| Add a sale record
GET /api/v2/products	| Get all products
GET /api/v2/products/id	| Get a single product
PUT /api/v2/products/id	| Update a single product
DELETE /api/v2/products/id	| Delete a single product
GET /api/v2/sales	| Get all sale records
GET /api/v2/sales/id	| Get a single sale record
PUT /api/v2/sales/id	| Update a single sale record





