# Charity Donation
A simple web aplication built with Django Framework.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [Setup](#setup)

## General Info
A web aplication, that allows users to donate unwanted items (e.g., clothes, toys, books) to trusted charity organizations.

## Technologies:
- Python
- Django
- JavaScript
- HTML
- CSS

## Features:
- user authorization (register, activate by e-mail, login, logout, edit profile, change password, reset password)
- choose categories and set the amount of donated items
- choose available organization, which will receive donation
- complete information about pickup date, time and address
- user panel with donation history
- admin panel
- handling a contact form

## Setup

First you should clone this repository:
```
git clone https://github.com/JKK86/charity_donation.git
cd  furniture_shop
```

To run the project you should have Python 3 installed on your computer. Then it's recommended to create a virtual environment for your projects dependencies. To install virtual environment:
```
pip install virtualenv
```
Then run the following command in the project directory:
```
virtualenv venv
```
That will create a new folder venv in your project directory. Next activate virtual environment:
```
source venv/bin/active
```
Then install the project dependencies:
```
pip install -r requirements.txt
```
Now you can run the project with this command:
```
python manage.py runserver
```

**Note** in the settings file you should complete your own database settings.

