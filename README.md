Django CMS template
=============================
Powered by Django CMS and a custom certification app prototype.
Originally proposed for the now defunct Health on the Net Foundation.

Pointers
--------
App Translation process
http://transifex.com -> Docs / Client

Django CMS
http://django-cms.org -> Docs and tutorial

Django Web Framework (for certification app)
https://www.djangoproject.com -> Documentation

Front-end Server and reverse proxy
http://nginx.com
http://wiki.nginx.org/Main

Backend Server
http://gunicorn.org

User registration
https://django-registration.readthedocs.org/en/latest/


CMS Server setup notes on Ubuntu
--------------------------------
Keeping server packages up to date

	sudo apt-get update
	sudo apt-get upgrade

Install packages

	sudo apt-get install\
		mysql-server\
		nginx\
		gunicorn\
		gettext\
		postfix\
		python-pip\
		python-django\
		python-mysqldb\
		python-lxml\
		python-imaging

Secure MySQL

	mysql_secure_installation

	create database hon character set utf-8 collate utf8_general_ci;

	mysql -u root -p

Configure nginx (Gzip, reverse proxy settings, SSL etc)

	sudo nano /etc/nginx/nginx.conf
	sudo nano /etc/nginx/sites-available/default
	sudo service nginx restart

Install CMS

	sudo pip install djangocms-installer
	sudo djangocms -p . hon
	sudo chown ubuntu:ubuntu -R hon static

Install user registration for Certification app

	sudo pip install django_registration

Create initial CMS database structure

	./manage.py syncdb
	./manage.py migrate

Get ready CMS static files (CSS, JS, icons)

	./manage.py collectstatic

Setup convenience on the command line

	nano .bash_aliases
	nano .inputrc
	source .bash_rc

Configure Upstart to start/stop and watch over Gunicorn, our python deployment server

	sudo nano /etc/init/hon.conf
	sudo service hon restart

Translations
------------
Create translation files (keeping the main .pot file to upload to Transifex)

	./manage.py makemessages --locale=de --keep-pot
	./manage.py makemessages --locale=fr --keep-pot
	./manage.py makemessages --locale=es --keep-pot
	cd ~/locale
	less django.pot

Updating translations
---------------------
Update message files after source code changes

	./manage.py makemessages -a --keep-pot

Push updates to translators using Transifex and get updates back continuously

	tx push ...POT file
	tx pull ...PO files

Compile translations for use (create .mo files from .po files)

	./manage.py compilemessages

Restart gunicorn after making changes to python code, translations or
substantial template changes

	sudo service hon restart

Allow to upload media files, make sure permissions are right

	mkdir media
	sudo usermod -a -G www-data ubuntu
	sudo chgrp -R www-data /home/ubuntu
	sudo chmod -R 2750 /home/ubuntu
	chmod -R 2770 /home/ubuntu/media
	chmod -R 2770 /home/ubuntu/static


Server distinction regex
------------------------
Used for routing traffic between EC2 CMS server or the Hospital one (Nginx configuration).

tested with: regexpal.com

	^/(static|media|en|fr|de|es).*$

Tests
-----
Legacy site (test redirects):

	/HONcode/
	/OESO/
	/pat_f.html
	/js/highlights_Lastconf1.js
	/images/banner_08_en.jpg
	/HonWebstyle_oct08.css
	/cgi-bin/HONcode/Inscription/site_evaluation.pl?language=en&userCategory=individuals
	/cgi-bin/HONnews/lasthonnews.pl?2009+1+Belgium
	/robots.txt
	/favicon.ico

New CMS:

	/
	/en/new-site
	/fr/
	/en/hello
	/de/hallo
	/es/ola
	/en/no-trailing-slash
	/media/document.pdf
	/media/photo.jpg
	/media/new-research.html
	/static/style.css
	/static/scripts.js
	/static/fb.png
