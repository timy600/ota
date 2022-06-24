# OTA Insight Test

## PART 1

### About the project
Simple Django CRM app with two models (User and Invoice)


#### Usage
Launch: 

```
cd OTA
python manage.py runserver 
```

Admin App: I've let the migrations and the sqlite.db I used. 
API Endpoints:

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

Django's views are where the mechanic is happening, but we will need to call on actions that affect the three apps (CRM, SA, PS) and their respective DBs everytime a change happens in one of them. The CRM is at the center of them, since a User is also a Customer or a Client in the other ones a change in the Invoices need to be reflected in both apps. 
This is the moment to think about separating the App Logic and the View Logic. We could use app.py as long as we separate by class according to the DB to be eventually modified. So two new app.py files in the apis folders with their classes: CallApiSalesAutomation, CallPaymentSystem; and a CRM equivalent, ControllerCRM. But a big change must also come from the admin.py file, since a change coming from the Admin Pages will imply a change in the SA and PS Apps. This will be one of the trigger to call one of the three previous classes. 

#### Jira tickets:
Low: refactor user/ endpoints (just move to a new folder)
High: access requests from the admin.py classes (InvoiceInline and UserAdmin).

### 2. Authentication
Since we'll interact with the two apps as Rest API, the Authentication process will pass by the request object in the views.py files.

We can use Django's Middleware "AuthenticationMiddleware" (see the MIDDLEWARE  in OTA/settings.py).
```python
django.contrib.auth import authenticate, login
```
Once the Login is established, we can us the decorator @login_required in the views needing one.

#### Jira tickets:
High

### 3. Sales Automation
Action Features, from CRM to SA:

- create customer: Originate from the Admin module. CallApiSalesAutomation.create_customer() that calls SA API POST customer. Should also call ControllerCRM.create_user().
- update customer profile fields: Originate from the Admin module. CallApiSalesAutomation.update_customer(), ControllerCRM.update_user()
- create Invoice: Originate from the Admin module. Since the status depends from the Payment System, the status will always be unpaid, CallApiSalesAutomation.check_invoice_status() must be called. If all invoices for this customer where paid until now, it will trigger CallApiSalesAutomation.update_customer() where the only field updated will be the last one. Also calls ControllerCRM.create_invoice().
- update customer Boolean payed Invoice field: Originate from apis/ps/views.py. Same as previous, calls CallApiSalesAutomation.check_invoice_status(), then CallApiSalesAutomation.update_customer(). Also calls ControllerCRM.update_invoice().

Action Features, from SA to CRM:

- create user: Originate from the apis/sa/view.py. ControllerCRM.create_user(), CallApiPaymentSystem.create_client().
- update user profile fields: Originate from the apis/sa/view.py. This should only update the fields related to the Customer Profile. The last field (cs_open_payment) value is not determined here. Calls ControllerCRM.update_user() and CallApiPaymentSystem.update_client().

#### Jira Tickets: 
High: build "create customer" and  "update customer" features
High: build "create user" and "update user" features  
Medium: change "create invoice" and "update invoice" features (need first to develop the PS).

### 4. Payment System

Action Features, from CRM to PS:

- create client: Originate from the Admin module or apis/sa/views.py. CallApiPaymentSystem.create_client() that calls PS API POST customer. Should also call ControllerCRM.create_user() but already developped in SA Part.
- update client: Originate from the Admin module or apis/sa/views.py. CallApiPaymentSystem.update_client(). Should also call ControllerCRM.create_user() but already developped in SA Part.
- create invoice: Originate from the Admin module. CallApiPaymentSystem.create_invoice() and ControllerCRM.create_invoice().

Action Features, from PS to CRM:

- update invoice status: Originate from apis/ps/views.py. Calls CallApiSalesAutomation.check_invoice_status() and ControllerCRM.update_invoice()

#### Jira Tickets: 
High: build "create client" and "update client"
High: build "create invoice" and "update invoice".
Medium: change "create user" and "update user"


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
