# OTG_Python_App_Engine
A simple project that demonstrates the minimal boilerplate needed to get a Google App Engine project started in Python. 

#Usage
Base files to start with for a Python-based App Engine project.  The project includes a partial Django template system for ease of display of data and values, and folders that house other files and packages to reduce dependancy coupling.  MVC-style organization of Python files for easier strategy changes to the backend code.

#Files
**app.yaml** - the main App Engine configuration file.  Built in static forwarders to folders for css, js, etc.

**main.py** - the primary view python file.  Houses the landing page, url handlers, and django render system.

**worker.py** - houses the main "guts" of the application.  Datastore models, memcache functions, and an example function are contained here.

#Folders
**templates** - where the html templates are stored for the django rendering system

**support_packages** - a place to store 3rd party python modules.  Useful for keeping codebase separate.

**backend_python_files** - a place for python files with their own API to sit, such that one may distribute the functionality to another server or service.  For advanced use, typically.

#Future additions
-Adding additional data store models and functions, as well as query systems

-Expanded use of the memcache system

-Blobstore functions for image and file storage/retrival

-CRON capabilities, such as daily database rebuilds

-Search and Geolocation services
