Bamboo Invoice on Centos with Nginx
###################################
:tags:  linux

`BambooInvoice <https://www.bambooinvoice.org/>`__ is free Open Source
invoicing software intended for small businesses and independent
contractors. It is easy to use and creates pretty good looking invoices.

It is a simple PHP application that is based on the CodeIgniter
framework. This means it is really simple to install on a typically LAMP
stack. I however use Nginx and could not find any notes on how to
configure it. It is pretty typical you can get most of the way by
reading any of the Nginx howto documents on the web. Personally, for PHP
apps, I use PHP-FPM, so you could use `this on
Howtoforge <https://www.howtoforge.com/installing-nginx-with-php5-and-php-fpm-and-mysql-support-on-centos-6.4>`__
to get most of the way. That will get you a working Nginx, PHP and MySQL
system.

Download the install file from [https://bambooinvoice.org/] an unzip is
in your www folder:

.. code:: bash

    cd /var/www
    wget https://bambooinvoice.org/img/bambooinvoice_089.zip
    unzip bambooinvoice_089.zip

You next step is to create a database for it along with a user:

.. code:: mysql

    CREATE DATABASE bambooinvoice DEFAULT CHARACTER SET utf8;
    GRANT ALL ON bambooinvoice.* TO 'bambooinvoice'@'localhost' IDENTIFIED BY 'bambooinvoice';
    FLUSH PRIVILEGES;
    exit

Now you can edit the config files to point at the database:

\`\`\`php
/var/www/bambooinvoices/bamboo\_system\_files/application/config/database.php
\`\`\`

Next you need set the base\_url in
``/var/www/bambooinvoices/bamboo_system_files/application/config/config.php``.
Nothing else is essential in that file, but read the docs in the ZIP
file to see what else you want to change.

Now the all important bit.

\`\`\`nginx /etc/nginx/conf.d/bamboo.conf server { listen 80;
server\_name bamboo.example; root /var/www/bambooinvoice/; index
index.php index.html; access\_log /var/log/nginx/bamboo\_access.log;
error\_log /var/log/nginx/bamboo\_error.log;

::

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }


    # Deny all attempts to access hidden files such as .htaccess, .htpasswd, .DS_Store (Mac).
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
     }
     location / {
         try_files $uri $uri/ /index.php$request_uri /index.php;
     }


     location ~ \.php($|/) {
         try_files $uri =404;
         fastcgi_pass 127.0.0.1:9000;
         include /etc/nginx/fastcgi_params;
         fastcgi_index index.php;
         set $script $uri;
         set $path_info "";
         if ($uri ~ "^(.+\.php)(/.+)") {
             set $script $1;
             set $path_info $2;
         }
         fastcgi_param URI $uri;
         # Next two lines are fix the 502 (Bad gateway) error
         fastcgi_buffers 8 16k;
         fastcgi_buffer_size 32k;

         fastcgi_param PATH_INFO $path_info;
         fastcgi_param SCRIPT_NAME $script;
         fastcgi_param SCRIPT_FILENAME $document_root$script;
      }

} \`\`\`

At first glance, there is nothing out of the ordinary. This is pretty
much what Howtoforge gives you. Look more closely and I have added the 3
lines 39-41. This solves a gateway problem I had when creating a client.
