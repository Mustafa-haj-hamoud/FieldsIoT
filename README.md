# Fields IoT

> Check out the live demo here: https://fieldsiot.pythonanywhere.com/


## What is Fields IoT?
Fields IoT is (as the name implies) a website that facilitates the implementation of internet of things, by creating online variables stored on the cloud. These variables can be easily and quickly updated and read via HTTP requests, which will be presented in the following paragraph


## Create an account with a Unique ID and Username
Once you create a new account, you will automatically be assigned a unique ID, which you will use to control your "fields" with HTTP requests


## What are fields?
Fields are basically online variables, you can update them manually with the website's GUT. Alternatively, you can update the values of fields by using GET requests in the following form
> http://fieldsiot.pythonanywhere.com/  update?  user_id=7  &  17=15  &  18=0

where the user_id is your user ID, field with id 17 will be assigned value 15, and field id 18 will be assigned value 0 .
You can later read these fields in JSON by using the "Generate API Link", which will return to you all your fields in JSON format, you can also use your own GET request, just don't forget to include your user ID in the request or you will be presented with an error, you can only read the values of fields created by that user ID.


## How do I use Fields IoT?
1. Head to http://fieldsiot.pythonanywhere.com/

1. Create a new account

1. Create all the fields you need to control your appliances

1. Use the generated API link to perform a GET request from your microcontroller or microprocessor in order to read all the fields and control your actuators according to the values of these fields

1. update your fields with google assistant or using any method that can utilize HTTP requests to change the values of these fields, changing with them the states of your devices accordingly


## What should I avoid when using Fields IoT?
Avoid making too many API requests, as it will overload the server, especially since it is hosted on a free hosting service for demonstration purposes, so the server is not as fast and responsive as it should be. If you want to update your fields, instead of making 1 request for each field, you can make a request that updates all the fields at once, and the same thing can be done for reading fields.


## Delete the fields you don't use
To make the demo lightweight and fast, once you're done using the field, you should delete it, or at least stop sending API requests for it


## Technical Info:
1. For the backend, Flask was used, and the web app was implemented on a free hosting service called pythonanywhere.com. If you are reading this file after a long while, the website may have gone offline

1. As a framework, Bootstrap 5.1 was used to make the website responsive and compatible with mobile devices, all the tables, the navbar, the buttons, and icons are from Bootstrap

1. The website uses a SQL database to store all the users, as well as the value of the each field assigned to each user, you can download a sample of this database from this repository and check the .schema structure for this page


Enjoy using Field IoT, all code and resources here are openly available so feel free to do whatever you want with it 😁
