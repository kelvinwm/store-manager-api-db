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
https://github.com/kelvinwm/store-manager-api
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
1.POST   /api/v2/auth/signup | Register a user
POST   /api/v2/auth/login | Log in user
POST   /api/v2/auth/logout | Log out user
POST  /api/v2/products | Add a product
POST  /api/v2/sales  | Add a sale record
GET  /api/v2/products | Get all products
GET  /api/v2/products/id  | Get a single product
PUT  /api/v2/products/id | Update a single product
DELETE  /api/v2/products/id | Delete a single product
GET  /api/v2/sales | Get all sale records
GET  /api/v2/sales/id | Get a single sale record
PUT  /api/v2/sales/id | Update a single sale record
DELETE  /api/v2/sales/id | Delete a single sale record
1.POST /api/v2/auth/signup |	Register a user
2. POST /api/v2/auth/login	| Log in user
3. POST /api/v2/auth/logout	| Log out user
4. PUT /api/v2/users/id |	Update user role
5. GET /api/v2/users	| get all registered users
6. POST /api/v2/category	| Add a category
7. GET /api/v2/category	| Get all categories
8. GET /api/v2/category/id	| Get a category by id
9. PUT /api/v2/category/id |	Update a category
10. DELETE /api/v2/category/id | Delete a category
11. POST /api/v2/products	| Add a product
12. POST /api/v2/sales	| Add a sale record
13. GET /api/v2/products	| Get all products
14. GET /api/v2/products/id	| Get a single product
15. PUT /api/v2/products/id	| Update a single product
16. DELETE /api/v2/products/id	| Delete a single product
17. GET /api/v2/sales	| Get all sale records
18. GET /api/v2/sales/id	| Get a single sale record
19. PUT /api/v2/sales/id	| Update a single sale record





