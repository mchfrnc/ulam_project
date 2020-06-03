# Amazon MVP
##### A very simple shop api

### Functionalities
The API allows users to place some orders for predefined products in the shop.

All products are assigned to categories. 

An authenticated user can add multiple (different or the same) products to a single order.
Every order can be modified and deleted by it's owner.

Some endpoints - Products and Categories - are available for everyone, and authentication is not required.

### Running the API

#### Prerequisites:
* Python3.7 or newer
* PostgreSQL
* All libraries from `requirements.txt` installed in Python's environment

##### Env variables
Before running the `manage.py` script, please make sure you have all required env variables set. These are:
`DB_USER`, `DB_PASSWORD`,`DB_HOST`, `DB_NAME`, `DB_PORT`.


##### Prepopulate categories and products
Optionally, after successfull installation of mentioned requirements, the script for populating data can be run: populate_data.py. 

```python
$ python manage.py shell -c "from populate_data import run; run()"
```

A couple of example products and categories will be added to the DB.


### Available endpoints and methods
> NOTE: normally I think I'd use Swagger or some other dedicated tool.

All endpoints starts with `<host:port>/api/`
```python
POST /auth/obtain_token/
{
	"username": "<username>",
	"password": "<password>"
}

Returns an authentication token.
```

```python
POST /auth/refresh_token/
{
	"refresh": "<token>"
}

Refreshes a token.
```

```python
GET /categories/ - Returns a list of all categories.
```

```python
GET /categories/<category_uuid>/ - Returns a single category's details.
```

```python
GET /product/ - Returns a list of all products.
```

```python
GET /product/<product_uuid>/ - Returns a single product's details.
```

```python
GET /orders/ - Returns a list of all orders placed by authenticated user.

POST allows to create a new order. Example payload:
{
    "items": [{"product": "cd70b008-a061-4b42-b990-cddb20b4baf4", "amount": 33}]
}
```

```python
GET /orders/<order_id>/ - Returns a single order details.

PUT allows to update existing order.

DELETE /orders/<order_id>/ - Deletes an order and it's order items
```

```python
GET /users/ - Returns list of registered users.
```


### What next?
The API is open for extension, for example for staff/management panel, which will allow to add new products and categories, modify existing orders (e.g. finalize the order) and user management.

The standard `manage.py runserver` should be replaced with some WSGI server.

Some additional integration tests should be performed.