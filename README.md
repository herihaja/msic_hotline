# msic_hotline
Referral Application Used by MSI's Hotline Staff 

# Setup - working on ubuntu - No guarantees about other OS's!

- First, ensure you are set up for **python development with pip and vitualenv**

- Ensure you have python installed and your system.
- Ensure `python --version` returns a version greater than or equal to 2.7 but less than version 3, then:

```
sudo easy_install pip
sudo pip install virtualenv
```

- Ensure you have installed postgres locally. 

- Clone **this repo**, then:

```
cd /path/to/repo/msic_hotline
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.pip
```

- Whenever you work on this project be sure to source `./venv/bin/activate` from the project directory.

- Now change `msic_hotline/settings.py` to use the database user you intend to use. If you don't want to use a password for this user then you will need to ensure that the following lines of `/etc/postgresql/9.3/main/pg_hba.conf` look as below:

```
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust 
```

^(if you are using IPv4)

- Now ensure that the `msic` database is created for the app and readable/writeable by your chosen user. You can create the database with either `createdb msic` or through the `psql` console.

- Now you should be able to syncdb, run migrations and load fixtures:

```
python manage.py syncdb # this will prompt for creation of an admin user. I believe this will then get blown away by either the fixture loading or the migration so don't worry about what you put. 
python manage.py migrate
```

- For fixtures you may not need to run in order but best to start with`python manage.py ./referral_system/fixtures/baseline.json` before running the others.

- Then:

```
python manage.py createsuperuser
```

- Follow the prompts and remember your answers. Then:

```
python manage.py runserver
```

- Navigate to `127.0.0.1:8000/referral_system/admin` and login. Click through to auth users and then your user and add a group before saving. "Hotline Counselor" seems to be a good one.

- Finally, navigate to `http://127.0.0.1:8000/referral_system/loginPage/` and log in as your auth user if necessary. You should be redirected to the referral form. A dashboard containing fixture data should also be visible if you click "VIEW MY REFERRAL"

- Enjoy!
