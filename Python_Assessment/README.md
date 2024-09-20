
For the implementation of the REST API I have used the Flask framework. Following are the packages that need to be installed in order the application to run:

>installing Flask
pip install Flask

>use flask forms 
pip install flask_wtf

> SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL
> work with data as Python objects
pip install Flask-SQLAlchemy 

> Flask extension that provides bcrypt hashing utilities
pip install flask-bcrypt

> provides user session management for Flask
pip install flask-login


To run the application go the project folder and use the following command. Then follow the "Running on" link that will appear on your console:

python -m flask run

I have created 3 users with the following credentials:

1) username: oli12 , password: password
2) username: test , password: password
3) username: testtest, password: password

You can of course create new users and new tasks for your testing using the Registration page.

I have focused on implementing the functionality so as you can see I kept the Frontend simple adding some minimal styling, using CSS and Bootstrap.
The core functionality (as per the requirements) was implemented and I have also implemented pagination for task retrieval (2 tasks per page).
