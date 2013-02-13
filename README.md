#INSTALLING A FLASK APP ON AWS
###with Ubuntu, Nginx, uWSGI, Virtualenvwrapper, and Git Flow.

##PREFACE

###Who Is This Tutorial For?

I wrote this tutorial for any Python developer looking to deploy a Flask app on AWS.  There are _many_ blog posts and tutorials already online that address this topic.  Granted, that's in part because there are so many dang variations--so many different ways to go about launching a Python app on AWS.  However, I discovered most of the resources presently online all seem to address the process in a semi-piecemeal fashion.  At the very least, many online tutorials, unfortunately, omit, or just poorly explain one or two critical steps in the process.  Moreover, none really provide the full breadth of detail required for a developer to not only configure an EC2 instance, but to also create a site accessible to an end-user via a custom domain.  In other words: a lot of tutorials fail to tie in the sysadmin / server configuration steps to the basic AWS components that create a functioning, consumer-facing app accessible in the browser.

This tutorial will not only get you familiar with the subtlties of configuring an EC2 instance for Flask, but will enable you to readily conquer all the little obstacles typically encountered while attempting to leverage AWS to make your dynamic web app visible at YourCustomDomain.com.

Nonetheless, I will make no claims that this tutorial is the _best_ method to get your Flask app up and running on Amazon.  It's just the method I prefer.  In the process of working through this tutorial, you'll garner the ancillary benefit of becoming vastly more comfortable with a few important components of Amazon Web Services if you are not already.

The tutorial assumes:
* You already have an AWS account, and have created an AWS Keypair and Security Group.
* You're comfortable using the command line of your terminal or SSH client to connect to a remote server.
* You're comfortable navigating the AWS Management Console via your browser.  

In some cases, it's arguably easier to launch your app on AWS via the Command Line Interface (CLI) of your terminal, SSH client, or preferred IDE.  However, using the AWS Management Console provides some instructional benefits of its own.  Moreover, not all the AWS command line tools are open source, and, more importantly, nearly each AWS service requires a separate tool--which means installing, configuring, multiple tools and keeping them up to date, etc.  AWS is working on improving the CLI experience for developers.  You can follow the progress of that effort here...
    
<http://aws.amazon.com/cli/>

Eric Hammon publishes a very helpful blog with regard to using Ubuntu with AWS. He's written a very helpful post on using the command line tools, which you can find here...

<http://alestic.com/2012/09/aws-command-line-tools>
    

###Why Ubuntu?

The Ubuntu EC2 instances come with Python 2.7 out of the box.  These AMIs are preconfigured by Canonical.  Whereas: the AWS Linux AMIs come with Python 2.6.  Trying to install Python 2.7 on one of Amazon's Linux AMIs, and then running both versions of Python is more intricate. Ensure you don't bork any number of things by picking one of the official Ubuntu instances configured by Canonical.  If you roll with another Linux AMI, you'll have to install 2.7, and preface all your commands with "python27" and make sure the appropriate version is indicated in the shebang for each of your .py files.

Are there caveats to using an Ubuntu instance on AWS EC2?

* Yes...it's faster on Heroku. (But then you'll likely move to AWS later if you scale.  You can use a Heroku instance from the AWS Marketplace, but this will increase fees.)
* Yes...it's faster on GAE. (But then you're heavily constrained by GAEs "rules of engagement"--i.e., your code will not be as easily deployable elsewhere.)
* Yes...you must depend on Ubuntu to update packages.

###Why Nginx?

Because Nginx has some performance benefits over Apache that might be useful if your Flask app suddenly gets a lot of traction.  Moreover, it's paired rather easily with uWSGI when deployed as a proxy server, which we'll sum up what a proxy server is something like this: 

1. Nginx receives a request from the end-user for a page on your website
+ Nginx sends a second "proxied" request to a specified server (in this case, the uWSGI application server--i.e., the "middleware"--that sits between your app and Nginx).
+ Nginx returns the result of that request back to the end-user.

So...we each time an end-user tries to dial up a page on your website, that request goes up a path from the client (i.e., the browser--Firefox, Chrome, IE, or whatever), to the proxy server (Nginx), to the application server (uWSGI), to the app (which has its own routing of requests to templates to deal with--since we're using a Flask app, then that routing happens via Werkzeug)...and all way back down from the application server, to the proxy server, to the client, where it is ultimately interprested by the end-user's eyeballs.  

That's demanding a lot from all the individual components.  Using Nginx as a front-end proxy to pass only essential requests to an application server is a smart way to provide a more stable experience for the end-user.  In this way, it functions like a fuse in an electrical current.  It helps keep the application server from getting overloaded with too many requests.


###Why uWSGI?

There are other application servers for Python apps.  A lot of these rely on something called Fast-CGI.  But Nginx plus uWSGI is a sort of force multiplier.  The two together allow for great stability and speed.

uWSGI is "middleware", and helps to optimize the means by which the web-server and app talk to  one another.

###Why VirtualEnvWrapper?

A virtual environment ("virtual env" or just "env" for short) serves as a sort of envelope or bubble, if you will, that contains all the necessary dependencies for your app.  It makes developing and deploying multiple apps on one machine much easier, because it helps to guard against the intermingling of the various versions and packages you'll install on a given machine to support your app.  VirtualEnvWrapper, as its name suggests, is a wrapper around your virtual environments.  It enables the fast and facile activation and switching between multiple virtual environments on the same machine.  Whenever a particular workflow requires the use of a virtual environment--as best practice usually requires--I usually also install VirtualEnvWrapper, as it makes it easier for me to use the same machine for other projects later on.

###Why Git-Flow?

Git-Flow is just a term to describe high-level repository operations for Vincent Driessen's branching model.  The primary benefit of a Distributed Version Control System (DVCS) is that it provides a safe and sane way to maintain your code, to track the contributions of individual developers, to merge those contributions together without creating a tangled nightmare, and to rollback mistakes during the development process, and, finally, to enable do all of these things concurrently and asynchronously, regardless of where individual developers might be located on the planet.  While Git is one of the reining methodologies for doing just that, if the folks you're working with don't have a common understanding about how to use Git, some relatively confusing situations tend to emerge pretty quickly. You can avoid this by having a clear and agreed upon strategy for various aspects of the typical Git workflow as code is pulled and pushed back and forth between your repository.  Git-Flow provides a model easily understood and rapidly adopted by most developers. You can learn more here:

<http://nvie.com/posts/a-successful-git-branching-model/>

<https://github.com/nvie/gitflow>

------------------------------------------------------------------------

##OVERVIEW
 
 * Selecting the Right EC2 Instance
 * Setting Up the Domain
 * Getting Ready to Scale
 * Configuring Your EC2 Instance
 * Update Your Instance / Install Dependencies
 * Install Nginx and uWSGI
 * Create Your App's Directory Tree
 * Prep for the Virtual Environment and Install Flask
 * Configure Your Virtual Environment
 * Launch the Virtual Environment
 * Create a Script to Serve Your App
 * Create a Module to Hold Your App
 * Create an Nginx Group, a uWSGI User, and Set Permissions
 * Configure Nginx
 * Configure uWSGI
 * Start the App!
 
 * Additional Tricks That Might Help
 * Acknowledgements

------------------------------------------------------------------------

###Selecting the Right EC2 Instance

Use _Ubuntu Server 12.04.1 LTS ami-3d4ff254_

Make sure your security group is associated with the EC2 instance before completing instance selection wizard.  You'll need to be sure your associated security group has port 80 (HTTP) open.

------------------------------------------------------------------------

###Setting Up the Domain

I like to do this earlier than later so I can verify I configured my EC2 instance, and the other supporting AWS services correctly.

You need to change DNS record with domain registrar to AWS Route53 DNS servers.

TODO: How to do this with GoDaddy.

Must properly configure Route53.

Must associate an Elastic IP (EIP) with new EC2 instance.


###Getting Ready to Scale

To use an AWS Load Balancer, use the Load Balancer's public URL for the A Record in Route53.

Make sure your health check in Load Balancer set to something appropriate...

I use:

    TCP:80
    Time Out: 5 seconds
    Interval: 30 seconds
    Unhealthy Threshold: 2
    Healthy Threshold: 2

You can also set up AWS CloudFront to serve up your site's JS scripts and static files from S3.


------------------------------------------------------------------------

##Configuring Your EC2 Instance

###Login Via SSH

Get SSH connection info from the EC2 Dashboard of the AWS Management Console...

    EXAMPLE: ssh -i /home/bluewolf/Keypairs/WordpressKeypair.pem ubuntu@107.21.97.86


If you get a message about wrong signature, nuke the existing with...

    EXAMPLE: ssh-keygen -f "/home/bluewolf/.ssh/known_hosts" -R 107.21.97.86
    

###Update Your Instance / Install Dependencies

    sudo apt-get update

Now is the time to install some dependencies.  Note: if you're running a plain AWS Linux AMI, you'd have to install these dependencies first...

    sudo apt-get install gcc autoconf libevent-dev libxml2-dev  libssl-dev libpcre++-dev libbz2-dev libcurl4-openssl-dev libgmp3-dev libmysql++-dev libmcrypt-dev

###Install Nginx and uWSGI

    sudo apt-get install nginx uwsgi uwsgi-plugin-python
    
###Create Your App's Directory Tree

I like to put my app's public facing files in /var/www...

    cd /var
    sudo mkdir www
    cd /www
    sudo mkdir concert1
    cd /concert1
    
TODO: Don't use the number one--i.e., "1"--in directory of file names because it's easily confused as the letter "l".

###Prep for the Virtual Environment and Install Flask

Return to the terminal, and install Python's setuptools...
    
    sudo apt-get install python-setuptools  
      
Install pip...

    sudo easy_install pip

Use pip to install your remaining dependencies...

    sudo pip install virtualenv virtualenvwrapper flask
    
###Configure Your Virtual Environment

    sudo nano .bashrc

Paste and save at the bottom of your .bashrc file...
------------------------------------------------------------------------

export WORKON_HOME=$HOME/.virtualenvs
   export PROJECT_HOME=/var/www
   source /usr/local/bin/virtualenvwrapper.sh
   
------------------------------------------------------------------------

Reinitialize bash...

source .bashrc

###Launch the Virtual Environment

    mkvirtualenv concert1
    
This command will cause VirtualEnvWrapper to simultaneously create and activate the env.  Depending on your set-up, you may alternatively execute _mkproject concert1_, which will make a virtualenv in _/home/ubuntu/.virtualenvs/concert1_ and create (or switch you over to a pre-existing) project directory with the same name in the _/var/www_ directory.

Alternatively, many tutorials suggest creating the virtual environment in the app's directory tree, like so... 

_/var/www/concert1/env_

That's perfectly acceptable, but it will require you to adjust the WORKON_HOME environment variable you just included in your .bashrc file, and will later require you to adjust a uWSGI parameter (UWSGI_PYHOME) accordingly.  Because the virtual environment is specific to a given system user, and will contain Python packages specific to a given app, and, moreover, because I may later choose to install other virtual environments specific to other apps and/or other users, to keep things straight, I like to name my virtual environment same as the associated app and place them in the home directory of the user.

###Create a Script to Serve Your App

Make sure you're in the /var/www/concert1 directory and create a script to run your app...

    sudo nano runserver.py

Paste and save the following into the new runserver.py file...
------------------------------------------------------------------------

from concert1 import app

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
  
------------------------------------------------------------------------

The if _ __name__ == '__main__' _ part allows us start up the app ourselves rather than through a uWSGI process, and allows us to access the app via the built-in development server.

###Create a Module to Hold Your App

Continue by typing these commands in the terminal...

    sudo mkdir concert1
    cd /concert1
    sudo mkdir static
    sudo nano __init__.py

Paste and save into the new __init__.py file...
------------------------------------------------------------------------

from flask import Flask
app = Flask(__name__)

@app.route('/')
def landing():
  return 'Hello, world!'
  
------------------------------------------------------------------------


Deactivate the env prior to proceeding with the following commands...

    deactivate

###Create an Nginx Group, a uWSGI User, and Set Permissions

First, create the nginx group...

    sudo addgroup nginx

Then, create a uWSGI user, and associate the new user with the Nginx group...

    sudo useradd -c 'uwsgi user' -g nginx uwsgi

Give uWSGI read permission to read the contents of scripts, and write permission to save compiled python files:

    sudo usermod -a -G nginx uwsgi
    sudo chown -R uwsgi:nginx /var/www/concert1
    sudo chmod -R g+w /var/www/concert1

###Configure Nginx

    cd /etc/nginx
    
Some tutorials suggest altering the nginx.conf configuration file in the _/etc/nginx directory_.  Alternatively, some tutorials suggest creating a configuration file in the _/etc/nginx/conf.d directory_.  Still other tutorials suggest altering the default configuration file in the _/etc/nginx/sites-available directory_.  Here's a good idea for newbs to sysadmin or server configuration in particular: _never_ alter, cut, or delete the contents of _any_ configuration file that ships with the software.  Make a copy of the file and save it with a different name first.  You can simultaneously copy and rename the file by doing...

cp <filename> <filename~>

My habit is to just append the filename with a tilde.  You can add a "_bak" or append the filename however you best see fit to mark it as a backup.  The point is: just keep a backup copy of any orginal config files that ship with Nginx in case something goes wrong.  

It's helpful to know that Nginx draws its configuration from three places...

The main config file is...

    /etc/nginx/nginx.conf
    
But in _that_ configuration file, you'll see the following code...

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;

These lines pulls into Nginx additional configuration settings from these two separate, additional directories.

In the primary _/etc/nginx_ directory_, you'll see those two directories.  You'll also see a _/sites-available_ directory.  (Note the difference between _sites-enabled_ and _sites-available_.) Thus: in the primary  _/etc/nginx_, you'll find one primary configuration file (_nginx.conf_) and three related directories containing additional configuration information..

    /etc/nginx
        nginx.conf
        /conf.d
        /sites-enabled
        /sites-available

Rather than mess with the top-level Nginx configuration settings located in the _nginx.conf_ file, instead, we'll place the new configuration settings specific to our app into one of the lower-level directories.  We could alter the _default_ configuration file that ships inside of the _/etc/nginx/conf.d_ directory.  A lot of tutorials suggest exactly that.  But, in keeping with conventions related to running multiple apps on one server, we'll put our app's specific configuration file in the _etc/nginx/sites-available_ directory.  Once we create our configuration file inside of the _sites-available_ directory, we'll then create a soft link or _symbolic link_ to the new configuration file we just made in the _/etc/nginx/sites-available_ directory.  By linking to the _sites-enabled_ directory, we'll tell the top-level _nginx.conf_ file to pull in and include these additonal configuration settings.  But, first, let's backup any default configuration file that ships with Nginx before we alter or replace it...

    cd /etc/nginx/sites-available
    sudo mv default default~
    
Now we'll create a new, empty default file...

    sudo nano default

Paste and save the following into the new default configuration file...

(A tip for Vim users: ctrl-6 at top of file; scroll to bottom; ctrl-k to cut all; copy the following code in this tutorial, then left-click to paste this code into the _default_ configuration file of your _/etc/nginx/sites-available_ directory.)
------------------------------------------------------------------------

server {
    listen              80;

    server_name         localhost;

    location /static {
        alias           /var/www/concert1/concert1/static;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/tmp/concert1.sock;
        uwsgi_param         UWSGI_PYHOME    /home/ubuntu/.virtualenvs/concert1;
        uwsgi_param         UWSGI_CHDIR     /var/www/concert1;
        uwsgi_param         UWSGI_MODULE    concert1;
        uwsgi_param         UWSGI_CALLABLE  app;
    }

    error_page          404     /404.html;

}

------------------------------------------------------------------------

TODO: explain what each of the config params does...

Once you've completed your update of this configuration file, enable your website by creating a symlink from sites-available to sites-enabled...

    sudo ln -s /etc/nginx/sites-available/concert1 /etc/nginx/sites-enabled/concert1

###Configure uWSGI

uWSGI necessarily makes fewer assumptions than Nginx about what you're trying to do, so we'll need to provide some baseline configuration information.  Ubuntu systems use the _/etc/init_ directory and and declarative config files within it as upstart settings. So, we'll create a _uwsgi.conf_ file in that directory to allow us to run uWSGI in the background.

    cd /etc/init
    sudo nano uwsgi.conf
 

Paste and save the following into the new configuration file...
------------------------------------------------------------------------

description "uWSGI"
start on runlevel [2345]
stop on runlevel [06]

respawn

exec uwsgi --master --processes 4 --die-on-term --uid uwsgi --gid nginx --socket /tmp/concert1.sock --chmod-socket 660 --no-site --vhost --logto /var/log/uwsgi/app/concert1.log

------------------------------------------------------------------------

Now, just as we did for Nginx, we need to include some additional configuration settings in an _apps-available_ directory for uWSGI, just as we did for Nginx.  We'll place these uWSGI configuration instructions in a _.ini_ file...

    cd /etc/uwsgi/apps-available
    sudo nano concert1.ini

Paste the following into the .ini file...
------------------------------------------------------------------------

[uwsgi]
plugins=python
vhost=true
socket=/tmp/concert1.sock

------------------------------------------------------------------------

And, again, just as we did for Nginx, enable these settings via a symbolic link to uWSGI's _apps-enabled_ directory...

    sudo ln -s /etc/uwsgi/apps-available/concert1.ini /etc/uwsgi/apps-enabled/concert1.ini

###Start The App!

sudo service uwsgi start
sudo service nginx start

uwsgi -s /tmp/uwsgi.sock --module myapp --callable app


Stop the app by logging out, then back into shell, and then...

    pkill -f "python runserver.py"
    
If you attempt to run the development server with...

    sudo python runserver.py
    
...and get an "address already in use" error, Nginx is probably already running.  You can kill it with...

    sudo killall nginx
    
If you attempt to run the development server, and the page hangs, double check your AWS security group settings to be sure port 80 (HTTP) is open.


------------------------------------------------------------------------

##ADDITIONAL TRICKS THAT MIGHT HELP

Armin Ronacher, the author of Flask, makes some important suggestions for deploying Flask with uWSGI...

http://flask.pocoo.org/docs/deploying/uwsgi/


If you're interested in using a different set-up than combining Nginx and uWSGI, you can proxy to a standalone servers written in Python (like Tornado)...

<http://flask.pocoo.org/docs/deploying/wsgi-standalone/>


For comparison sake, here are some instructions for running Flask on a standard Linux AMI using a YAML uWSGI config file...

<https://github.com/d5/docs/wiki/Installing-Flask-on-Amazon-EC2>

...and...

<http://blog.iqyax.org/configuring-multiple-flask-sites-with-uwsgi-and-nginx-on-an-amazon-ec2-instance>


Want to speed up the process?  Check out Jeff Hull's thirty-minute-app, which installs a Flask app on a basic Linux instance by leveraging GitHub, Fabric, and Boto...

https://github.com/jsh2134/thirty-min-app


And here's another rapid deply option, but using Apache, mod_wsgi, and Fabric by Swaroop C. H....

https://github.com/swaroopch/flask-boilerplate


If you're thinking about incorporating some devops utilities into your setup, checkout Matt Wright's use of Ansible...

<http://mattupstate.github.com/python/devops/2012/08/07/flask-wsgi-application-deployment-with-ubuntu-ansible-nginx-supervisor-and-uwsgi.html>


Some uWSGI wisdom...

<http://uwsgi-docs.readthedocs.org/en/latest/Nginx.html>

<http://uwsgi-docs.readthedocs.org/en/latest/ThingsToKnow.html>

<http://library.linode.com/web-servers/nginx/python-uwsgi/ubuntu-10.04-lucid>

To get all the command line options for launching uwsgi...

    uwsgi --help


Location of all virtual envs...

    /home/ubuntu/.virtualenvs


The location of Python packages specific to your app...

_~/.virtualenvs/concert1/lib/python2.7/site-packages_


List all virtual envs by using this virtualenvwrapper command...

    workon
    
    
List all system users...

    cat /etc/passwd | cut -d ":" -f1
    

List all groups for a user...

    groups <user>
    

List all users for a group...

    sudo apt-get install members
    members <group>
    

List all installed packages...

    pip freeze -l
    

To delete everything in a file using vi...

esc
:1,$d

...then right-click inside vi to paste from clipboard.

------------------------------------------------------------------------

TODO:  Adjust this...

You can also use uWSGI as an http server, for testing purposes. If you have a copy of your website checked out in the current directory, you can run

uwsgi --http 127.0.0.1:9090 --pyhome ./env --module application --callable app

------------------------------------------------------------------------

##ACKNOWLEDGEMENTS

Conrad Kramer has written one of the most influential blog posts for install Flask on EC2, and I borrow liberally from this post...

<http://blog.kramerapps.com/post/22551999777/flask-uwsgi-nginx-ubuntu>

Likewise, Eric Taubeneck, influenced by Kramer's blog, has a good variation on these instructions...

<http://skien.cc/blog/flask-nginx-uwsgi>

This anonymous author also provides some instruction based on Conrad Kramer's original blog...

<http://www.collectivedisorder.com/ubuntu>

Finally, Leonids Maslovs has a very good tutorial here...
<http://leonardinius.galeoconsulting.com/2012/09/python-playground-part-2-deploying-flask-app-on-ubuntu-nginx-uwsgi-supervisor-git/>

