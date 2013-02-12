==============
Concert Talent
==============


******************************************************************************************************

**A dead simple app for finding and hiring professional musicians.**

******************************************************************************************************

Copyright (c) 2013 by Concert Talent.  All Rights Reserved.

:license: See LICENSE below for more details.

******************************************************************************************************


Code was liberally borrowed from...

https://github.com/dracule/FlaskBootstrapSecurity

...and mashed up with...

https://github.com/Bravoflix/Canteen/tree/master/src

******************************************************************************************************

Included herein are User Groups and Permissions, User Registration, Roles, Mail, a variety of script commands, and, yes, even Twitter Bootstrap...ready for you to orchestrate your magnum opus. :)

Please note: you must include a legit Gmail or Google Apps e-mail address in the app's config file for new user registrations to work properly.

******************************************************************************************************

INSTALLATION
============

To hack at this code base on your local machine.

1. Clone this repo from GitHub...

    git clone git@github.com:Bravoflix/Concert_Talent.git

2. Change your working directory to the cloned repo now sitting on your local machine.

    cd concert_talent

3. The following assumes you've already got virtualenv set up on your local machine, and now require VirtualEnvWrapper. Info on using virtualenv wrapper is available on the private Redmine wiki. Take a look at those docs...but elsewise it's easy to install virtualenv wrapper simply by:

    pip install virtualenvwrapper

4. Follow up with a few added lines of code to your ~/.bashrc file... These changes will enable virtualenv to work upon your shell's startup. MyDevProjectsDirectory is whatever you prefer as your standard Python or web development projects directory.
        
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/MyDevProjectsDirectory
    source /usr/local/bin/virtualenvwrapper.sh

5. Now restart the shell...

    source ~/.bashrc
    
6. Using virtualenv wrapper, create a virtual environment

    mkvirtualenv srconcert_talentenv

7. Make sure you've already navigated to the local directory representing the repo you just cloned and downloaded...and install the required dependancies:

    pip install -r requirements.txt

8. Go to `concert_talent/config.py` to change your mail server and other settings; edit the Config(object) class.

    NOTE: *As mentioned above, presently, you need a legitimate Gmail or Google Apps for Your Domain account in the MAIL USERNAME and DEFAULT MAIL SENDER, as well as a real password in the MAIL PASSWORD in order for new user registrations to work.*:

9. Prepare the SQLAlchemy Database:

    python manage.py reset_db

    python manage.py populate_db

10. Run the development server to see the app on your local machine at http://127.0.0.1:5000...
        
    python manage.py runserver


**Commands included with Flask-Security...**

* ...can be found at the URL below, and by looking in the `concert_talent/script.py` file that comes with this app.: 

    http://packages.python.org/Flask-Security/#flask-script-commands 

******************************************************************************************************

TEMPLATES
=========

The base template is a spin-off of the Canteen template (Flask + Compass + Bootstrap).  It's located at: `concert_talent/templates/base.html`

******************************************************************************************************

"CHAFFIFYING" UNIQUE OBJECT IDs
===============================

* You may not want simple URLs revealing the order of object ids (for instance, user ids). 

* For example, you might feel this is less than ideal:
    
    http://example.com/users/view/1/

* So you can use `encode_id` and `decode_id` found in `concert_talent/helpers.py` to fix that, so, instead of...

    http://example.com/users/view/1/
        
* ..you'll get something like...

    http://example.com/users/view/w3c8/

******************************************************************************************************

LICENSE
=======

Copyright (c) 2013 by Concert Talent.  All rights reserved.

This code and all files associated with it are property of Concert Talent.

For internal use only!
