# OTA Insight Test

## PART 1

### About the project
Simple Django CRM app with two models (User and Invoice)

### Project Structure

### Getting Started

#### Prerequisites

#### Installation

#### Usage
- Launch
- Admin App
- API Endpoints

```
crm/user: retrieve list of users with id
crm/user/<user_id>/invoices: retrieve unpaid invoices
```

#### Response: Limit to 10 per minute

For limiting the number of request one can do per minute, we need three things:

- get the IP address
- handle timely request
- get a count per origin and per minute
    
The IP address can be accessed in the "request" element in the views. With request.META.get(), with either HTTP_X_FORWARDED_FOR or REMOTE_ADDR.

Where to call it? The simple straightforward answer is to create a decorator function in the utils.py file. But it's better to create a whole Middleware, saving the requests, their IP and time.
In the case that their would be an Authentication process for using the API, it allows to use the Authentication Middleware. This way following the User instead of the IP.

By implementing it as a decorator we could choose between a limit per endpoint or for the whole API when more routes are added.  

## PART 2
Sales Automation (SA) and Payment System (PS) integration

### 1. Directory Structure and URL routes
To interact with both apps we will separate further the API routes in our URLs list and reflect this in our folder disposition.
Inside the `apis` folder we can create one folder per app, with at least two files in each one: urls.py (with the list of endpoints) and views.py. In Flask I would call that a Blueprint but I don´t know what is the exact term used in Django. Those urls root word would be included in urlpatterns of crm/urls.py, next to user (which would have its own folder, and its views would be moved there).
The endpoints would look like this:

/admin/...

/api/user/<user_id>

/api/sa/...

/api/ps/...


#### Jira tickets:
Low: refactor user/ endpoints (just move to a new folder)
High: modify user/invoice models


### 2. Authentication
Since we'll interact with the two apps as Rest API, the Authentication process will pass by the request object in the views.py files.

We can use Django's Middleware "AuthenticationMiddleware" (see the MIDDLEWARE  in OTA/settings.py).
```python
django.contrib.auth import authenticate, login
```
Una vez establecido un login, se puede usar el decorador @login_required para las views que necesitan uno.

#### Jira tickets:
High

### 3. Sales Automation
From CRM to SA:

- create customer
- update customer profile fields
- update customer Boolean payed Invoice field

From SA to CRM:

- create user
- update user profile fields
- update invoice Boolean payed Invoice field

Adapt the API CRM User:

In urlpatterns, add the following endpoints:

```
GET/POST: /api/user/
GET/POST: /api/user/
PUT/DELETE: /api/user/<crm_user_id>

GET/POST: /api/sa/
PUT/DELETE: /api/sa/<crm_user_id>
```

In views.py
Methods: add CRUD methods for User and Invoice.

### 4. Payment System

From CRM to PS:

- create client
- update client
- create invoice

From PS to CRM:

- update invoice status


### 5. Parsing Data and Serialization
If we just stop here, the model file will get longer and longer. The best practice to handle the data is to serialize and create schemas.
For both app, the data are passed in a JSON Format. So far, it was easy to recreate simple Entity from the model and pass a JSON format like dictionary.

#### Jira ticket:
Medium.

### 6. Documentation
The first part of the project only required one API endpoint, a simple GET. With the multiplication of endpoints, having a proper Documentation to know the input and output formats (especially for the POST, PUT and/or PATCH endpoint inputs) will be crucial.

The most best tech right now would be to integrate Swagger. It can be implemented with django-rest-swagger. It's a swagger/OpenAPI Documentation Generator library.
I used it with Flask, it was really neat. The other option is ReDoc.

#### Jira ticket:
Medium: implementing the template for the html view and its own url patterns.
Low: every schema docs.