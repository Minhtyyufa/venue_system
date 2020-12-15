# Back-end Server for the Venue System
To get the server up and running, first clone the repository. Navigate into this directory [/db_final](/db_final).

To install your dependencies run:

```
pip install requirements.txt
```

If you are running the server on a Windows machine, you may have to install additional dependencies for Django.

You will then need to create a MySQL database for the project. Create a new database called "venue_system"

Then navigate to the settings_copy file located here [settings_copy.py](/db_final/db_final/settings_copy.py). Rename this file to [settings.py]().
Open the file and change this line to match your Django secret key for the project.

```python
SECRET_KEY = "<DJANGO SECRET KEY>"
```

If you don't have a secret key you can generate one by running this command:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then in the same [settings.py]() file navigate down to the section that looks like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': "venue_system",
        'USER': '<USER FOR DATABASE>',
        'PASSWORD': '<PASSWORD FOR DATABASE>',
        'HOST': '<HOST>',
        'PORT': '<PORT>',
    }
}
```

Change the values of this dictionary to match your configuration of your database. 

In your terminal, run these commands from the [/db_final](/db_final) directory.

```
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

After this your server should be up and running!