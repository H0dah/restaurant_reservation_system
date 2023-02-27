
## Installation

First, start by closing the repository:

```
git clone https://github.com/TheHive-Project/TheHiveHooks.git
```

We recommend to use `virtualenv` for development:

- Start by installing `virtualenv` if you don't have it
```
pip install virtualenv
```

- Once installed access the project folder
```
cd restaurant_reservation_system
```

- Create a virtual environment
```
virtualenv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

- Start the web application
```
python manage.py runserver
```

## App Usage

- to create superuser write on terminal inside virtual env
```
python manage.py createsuperuser
```

- to create an employees, bookings, tables, go to browser and navigate to:
```
http://127.0.0.1:8000/admin
```
and login with credentials of user you created in last step


- to create accounts use admin page(in last step) and connect them to an user


## App Structure
```
user ---has---> account (one to one relationship)

table --has--> bookings (can be more than one)
```

## POSTMAN
```
postman collection file in the root directory called--> postman_collection.json
```
