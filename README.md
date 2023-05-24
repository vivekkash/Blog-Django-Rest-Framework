# Blog-Django-Rest-Framework
A blogging Rest API's created using Django Rest Framework.

[![N|Solid](https://www.django-rest-framework.org/img/logo.png)](https://www.django-rest-framework.org/)


## Introduction:
This is module is only for learning purpose, and should be used in development environment, however if you want to use on production platform, kindly ensure its well tested and do it on your own risk.


## Features

- User Registration
- User Authentication
- Authencticated and Authorized Users can create, view, update and delete their respective blog posts
- Publicly view access for all the blogs available.
- Search specific blogs.


## List of API's

| # | API's | Methods | Descriptions | 
|---|------------|---------|--------------| 
|1 | login | POST | Authenticate the user |
|2 | register | POST | Register new user |
|3 | blogs | GET | Fetch all the blogs |
|4 | blogs/?s=key | GET | Fetch the blogs matching the key |
|5 | blogs/?page=[1,2,..] | GET | Pagination for the blogs |
|6 | blog | GET, POST, PUT, DELETE | Allow authorized and authenticated user to do CRUD ops|
|7 | blog/?s=key | GET | Allow authorized and authenticated user to search their blogs matching with key|


## Installation

1. Git Clone 
    ```sh
    https://github.com/vivekkash/Blog-Django-Rest-Framework.git
    ```

2. Create a virtual environment
    ```sh 
    python -m venv venv 
    ```
    
3. Activate the virtual environment 
    ```sh
    source venv/bin/activate
    ```
  
4. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```
5. Run the server
    ```sh
    python manage.py runserver
    ```
6. Goto the browser and check the below
    ```sh
    http://127.0.0.1:8000/blogs
    ```
    
