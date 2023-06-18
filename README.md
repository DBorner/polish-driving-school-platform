# Polish driving school django platform
Simple platform for Polish driving school made with Django 

![Default Home View](__screenshots/home1.png?raw=true "Title")
![Default Home View](__screenshots/home2.png?raw=true "Title")
![Panel View](__screenshots/panel.png?raw=true "Title")
![Course Detail View](__screenshots/panel_course_detail.png?raw=true "Title")

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/DBorner/polish-driving-school-platform.git
    
Create .env file:

    HOSTS={your allowed hosts}
    DJANGO_SECRET={your django secret}

Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt

Go to project folder:

    $ cd oskplatform
    
Then simply apply the migrations:

    $ python manage.py migrate
    
Create super user:

    $ python manage.py createsuperuser

You can now run the development server:

    $ python manage.py runserver
