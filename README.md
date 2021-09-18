# Full Stack Developer Nano Degree Capstone Project

# Pricelee

Pricelee is a price tracking website. It allows you to search products from popular online stores and to create alerts for the products you want to track after you sign up. You can use filters to improve the search and get more specific results. The store manager can add more filters to the frontend as the developer completes their implementation and testing.

For the moment, pricelee only supports calls to the ebay api. It can search by keywords, category id, and price range. The api can also search for a specific product by item id in order to update stored products periodically.

After a user is authenticated, they can add alerts, edit and delete them. They can see the complete list of the alerts they created, and their most recent alerts.

The landing page displays sponsered products added by the admin only.

The website is hosted on [https://pricelee.herokuapp.com/](https://pricelee.herokuapp.com/)

# Frontend

- This is a single page application. The frontend consists of a single html template, - rendered by the Jinja2 engine - in the templates folder, in addition to css and javascript folders in the static folder. Most of the functionality is written in vanilla javascript and occasionally JQuery. 
- `index.html` is a template downloaded and adapted from [https://startbootstrap.com/](https://startbootstrap.com/). The design is made with the Bootstrap 5 library.

- The auth0-spa-js library is used on the frontend to authenticate users and get user information.

Below are the sources for code snippets I adapted from the internet:
- The Auth0 authentication logic: [https://ckinan.com/blog/auth0-simple-example-vanilla-js/](https://ckinan.com/blog/auth0-simple-example-vanilla-js/)

- Checking form validity: [https://getbootstrap.com/docs/5.1/forms/validation/](https://getbootstrap.com/docs/5.1/forms/validation/)

- Pagination logic: [ https://codepen.io/kshoeb/pen/NQboaL]( https://codepen.io/kshoeb/pen/NQboaL)

- Checking the existance of an element on the page: [https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists/47776379](https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists/47776379)

## Dependencies

- JQuery and auth0-spa-js links is included in the `index.html` file, and Bootstrap is included in the css folder.

# Backend

The backend main modules are: app.py, modules.py, and request_ebay.py

## Dependencies

1. **Python 3.9.7** - Follow instructions to install the latest version of python for your platform in [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the project directory  and running:
``` pip install -r requirements.txt ```
This will install all of the required packages we selected within the `requirements.txt` file.

## Configuration

- Configure your app in `config.py`.
Inside this file, setup environment variables to connect to your database server, configure your stores api and Auth0 credentials.
- configure you Auth0 `/authorize` call in `auth_config.json`

## Database setup

Create tables by running  ```flask db upgrade``` in your terminal.

### Running the server

From within the project's main directory first ensure you are working using your created virtual environment.
Each time you open a new terminal session, run:

``` export FLASK_APP=app.py ```

To run the server, execute:

``` flask run --reload ```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

- The testing module contains valid tokens to test endpoints that require permissions.
- The function db_drop_and_create_all in `models.py` creates demo rows for testing purposes.
- To create the demo rows, make sure the line db_drop_and_create_all(db) in app.py is not commented out.
- To run the tests, execute the following command:
``` python test_flaskr.py ```

## Roles

- Some endpoints require permissions which are defined in roles. Those roles are assumed by certain users through your Auth0 api.

### Store Administrator

- Can add sponsered deals to the landing page and add search filters.
- Permissions: 
    - `post:deals`
    - `post:filters`

### Store Manager

- Can add search filters to enhance search results precision.
- Permissions: 
    - `post:filters`

## Endpoints

- GET '/auth_config'
- GET '/filters'
- POST '/user'
- POST '/alerts'
- POST '/alerts/add'
- POST '/recent_alerts'
- POST '/search'
- POST '/filters'
- POST '/deals'
- PATCH '/alerts'
- DELETE '/alerts'

### GET '/auth_config'
- Fetches auth_config.json file and sends it to the frontend to format the Auth0 `/authorize` request.

### GET 'filters'
- Fetches available filters from the database
- Returns a list of filters.
``` 
    {
        "success": True,
        "filters": ['category', 'price']
    }
```

### POST '/user'
- Looks up the current authenticated user and adds if not present.
- Sample request: curl 'http://127.0.0.1:5000/user' -X POST -H 'Content-Type: application/json' -d '{"user_id": "112442572274179169362",
    "user_name": "khadidjaarezki999", "email": "khadidjaarezki999@gmail.com"}'

### POST 'alerts'
- Fetches current authenticated user's paginated alerts from the database
- The user must be logged in to send the request.
- Returns a list of paginated alert objects.
- Sample request: curl 'http://127.0.0.1:5000/alerts' -X POST -H 'Content-Type: application/json' -d '{"user_id": "112442572274179169362",
    "page_number": "1"}'
- Sample response:
```
{
    "success": True,
    "user-alerts": [
        {   'alert_id': 2, 
            'desired_price': 25.0, 
            'product_name': 'For 2020 MacBook Pro Air 13” A2338 A2337 laptop sleeve bag handbag carry pouch', 
            'product_link': 'https://cgi.sandbox.ebay.com/2020-MacBook-Pro-Air-13-A2338-A2337-laptop-sleeve-bag-handbag-carry-pouch-/110538066270?var=0', 
            'product_image': 'https://thumbs1.sandbox.ebaystatic.com/pict/04040_0.jpg', 
            'price_difference': 0.0, 
            'product_price': 15.99, 
            'product_currency': 'USD', 
            'product_store': 'ebay'
        }
    ]
    "total_items": len(alerts)
}
```
### POST '/recent_alerts'
- Fetches current authenticated user's most recently created alerts from the database.
- The user must be logged in to send the request.
- Returns a list of paginated alert objects filtered by their creation date.
- Sample request: curl 'http://127.0.0.1:5000/recent_alerts' -X POST -H 'Content-Type: application/json' -d '{"user_id": "112442572274179169362",
    "page_number": "1"}'
- Sample response:
```
{
    "success": True,
    "user-alerts": [
        {   'alert_id': 2, 
            'desired_price': 25.0, 
            'product_name': 'For 2020 MacBook Pro Air 13” A2338 A2337 laptop sleeve bag handbag carry pouch', 
            'product_link': 'https://cgi.sandbox.ebay.com/2020-MacBook-Pro-Air-13-A2338-A2337-laptop-sleeve-bag-handbag-carry-pouch-/110538066270?var=0', 
            'product_image': 'https://thumbs1.sandbox.ebaystatic.com/pict/04040_0.jpg', 
            'price_difference': 0.0, 
            'product_price': 15.99, 
            'product_currency': 'USD', 
            'product_store': 'ebay'
        }
    ]
    "total_items": len(alerts)
}
```

### POST '/alerts/add'
- Creates a new alert for the submitted product and stores it.
- The user must be logged in to send the request.
- If the alert product is not stored, it adds it to the database.
- Sample request: curl 'http://127.0.0.1:5000/alerts/add' -X POST -H 'Content-Type: application/json' -d '{"product_id": "110537674650", "product_image": "", "product_name": "Highlights Hidden Pictures Puzzle Collection: 10-book Wedge", "product_link": "https://cgi.sandbox.ebay.com/Highlights-Hidden-Pictures-Puzzle-Collection-10-book-Wedge-/110537674650", "product_price": "USD 24.99", "product_store": "ebay", "desired_price": "20", "user_id": "112442572274179169362"}'

### PATCH '/alerts'
- Updates an alert filtered by the provided id
- The user must be logged in to send the request.
- Sample request: curl 'http://127.0.0.1:5000/alerts' -X PATCH -H 'Content-Type: application/json' -d '{"user_id": "112442572274179169362", "new_desired_price": "22", "alert_id": "1"}'

### DELETE '/alerts'
- Deletes an alert filtered by the provided the id
- The user must be logged in to send the request.
- Sample request: curl 'http://127.0.0.1:5000/alerts' -X DELETE -H 'Content-Type: application/json' -d '{"alert_id": "2", "user_id": "112442572274179169362"}'

### POST '/search'
- Sends request to online stores to search for products by keywords and/or filters.
- Returns a list of product objects that match the search.
- Sample request: curl 'http://127.0.0.1:5000/search' -X POST -H 'Content-Type: application/json' -d '{"keywords": "book", "filters": "{"location": "", "categoryId": "", "store": "ebay", "min_price": "", "max_price": ""}",   "page_number": "1", "user_id": "112442572274179169362"}'

- Sample response: 
```
{
    "success": True,
    "search-results": [
        {
            'product_store': 'ebay', 
            'product_name': 'Test Xiamomi Google Pixel', 
            'product_id': '110538079509', 
            'product_link': 'https://cgi.sandbox.ebay.com/Test-Xiamomi-Google-Pixel-/110538079509', 
            'product_currency': 'USD', 
            'product_price': '99.0', 
            'product_image': ''
        }, 
        {
            'product_store': 'ebay', 
            'product_name': 'Test Multi Lenovo OnePlus One Windler-Carroll 52', 
            'product_id': '110538099562', 
            'product_link': 'https://cgi.sandbox.ebay.com/Test-Multi-Lenovo-OnePlus-One-Windler-Carroll-52-/110538099562?var=0', 'product_currency': 'USD', 
            'product_price': '1000.0', 
            'product_image': ''
        }
    ]
    "total_items": 100
}
```

### POST '/filters'
- Adds new search filters to the database
- Requires permission: `post:filters`
- Sample request: curl 'http://127.0.0.1:5000/filters' -X POST -H '{"Content-Type": "application/json", "Authorization": "Bearer {manager_token}"}' -d '{'filter': 'price'}'

### POST '/deals'
- Adds a new sponsered deal to the database.
- Requires permission: `post:deals`
- Sample request: curl 'http://127.0.0.1:5000/deals' -X POST -H '{"Content-Type": "application/json", "Authorization": "Bearer {admin_token}"}' -d '{'deal_name': 'Dell 27 Curved Gaming Monitor - S2722DGM Featuring FreesSync Premium', 'deal_link': 'https://deals.dell.com/en-us/productdetail/ag5n', 'deal_image': 'https://snpi.dell.com/snp/images/products/large/en-us~210-AZZP/210-AZZP.jpg', 'deal_price': '299.99', 'deal_currency': 'USD', 'deal_store': 'Dell'}'

## Authors: Khadidja Arezki
