# invoicemanagement


**Pre-Requisites**

Pycharm

Ubntu/Windows

Python3.10

Virtual environment


**Installing the Project**

Create the virtual environments using **python3 -m venv environment_name**

Activate the venv by running this: source {your env name}/bin/activate

Install the required packages mentioned in the requirements folder pip install -r requirements/requirements.txt



**Django Specific configurations**

Populate DB using below commands:

python manage.py makemigrations

python manage.py migrate



**Start server using below command:**

python manage.py runserver

Create superuser

Create a superuser or access the Django management shell.

python manage.py runserver



**Note:**

To avoid commit python compiled files(.pyc) files please add these into .gitignore file *.pyc

Before commit the code please use pep8 check. please refer below url:

https://www.python.org/dev/peps/pep-0008/
we can use PyCharm(editor) Code -> Inspect Code utility for pep8 guideline.
