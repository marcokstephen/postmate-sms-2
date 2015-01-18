#### Install Dependencies ####
First, `cd` into the project directory.  
Install `virtualenv` with `sudo easy_install pip`, then `sudo pip install virtualenv`  
Set up a virtual environment: `virtualenv --distribute venv`  
Activate it: `source venv/bin/activate`  
Install twilio: `pip install twilio`  
Deactivate virtual environment: `deactivate`  
Link dependencies to your project:
```
ln -s venv/lib/python2.7/site-packages/twilio .
ln -s venv/lib/python2.7/site-packages/six.py .
ln -s venv/lib/python2.7/site-packages/httplib2 .
ln -s venv/lib/python2.7/site-packages/requests .
```

Now, you can run the project locally with `./dev_appserver.py <path_to_project>`  
or deploy it with `./appcfg.py update <path_to_project>`

