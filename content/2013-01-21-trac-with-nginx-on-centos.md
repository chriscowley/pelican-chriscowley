---
layout: post
title: "Trac with Nginx on Centos"
date: 2013-01-21 11:53
comments: true
categories: linux
---
[Trac](tac.edgewall.org) is an excellent online project management tool. Nginx us a great web server. Surely the combination of the two should be a match made in heaven. I would say so, although there are a couple problems. The easiest way to deploy Trac is on Apache using mod_wsgi or FastCGI. This option does not really exist for Nginx. Okay, it can do FastCGI, but I have not get that set up on my server.
<!-- more -->

What Nginx does do extremely well is Proxy stuff. Use this with Trac's built in web server (tracd) and you have  a very nice little set up. Ruby people, before you get all upset, Trac's server is not just for dev (a la WEBrick). It is fine for production use.

The first thing to do (obviously) is to install Trac. I get it from Pip, although a slightly older version is in [EPEL](http://fedoraproject.org/wiki/EPEL) if you prefer to stick with native packages.

```
sudo yum install python-setuptools
sudo pip install Trac
sudo useradd -r -d /var/local/trac trac
sudo -u trac trac-admin /var/local/trac/trac.example.com initenv
sudo -u trac htpasswd -c /var/local/trac/.htpasswd example-realm chris
```

Answer the little question it asks you - this includes the VCS you want to use, but that is for another day. I use the TracGit plugin to link to my Git repos.

Create an init script (`/etc/init.d/trac`) that contains something like:

{% gist 4586539 %}

Start up the Trac daemon and enable it on boot up

```
sudo chmod +x /etc/init.d/trac
sudo chkconfig trac on
sudo /etc/init.d/trac start
```

Open it up and have a look at least. You will probably want to modify it to use your authentication realm.

Now you need to configure Nginx. I use the package from [EPEL](http://fedoraproject.org/wiki/EPEL). Enable that if you have not already and run 

```
sudo yum install nginx
```

Create the file `/etc/nginx/conf.d/trac.conf` containing something like:

{% gist 4586630 %}

Finally enable Nginx on boot up and start it:

```
sudo chkconfig nginx on
sudo server nginx start
```

