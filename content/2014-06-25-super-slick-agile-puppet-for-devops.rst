Super Slick Agile Puppet for Devops
###################################

:date: 2014-06-25 21:22 
:category: puppet :tags: devops, puppet
:slug: super-slick-agile-puppet-for-devops

.. figure:: {filename}/images/3SJXbMb.jpg 
    :align: right
    :width: 300px

With a superb buzzword laden title like that, then I reckon massive
traffic boost is inevitable.

Puppet is my favourite Configuration Management tool. This is not a post
to try and persuade anyone not to use Ansible, Chef or any other. What I
want to do is show I build Puppet based infrastuctures in such away that
it meets all the basic tenets of DevOps/Agile/buzzword-of-the-month.

What to we need:

-  CentOS 6 - RHEL/CentOS is pretty much the defacto enterprise distro.
   This will easily translate to Debian/Ubuntu or anything else.
-  Puppet 3 - I like a traditional Master/Agent set up, if you prefer
   master-less good for you. This is my blog, my rules.
-  Git
-  Dynamic Environments
-  PuppetDB
-  Hiera
-  Jenkins

All the config is stored in Git, with Jenkins watching it.

Puppet tends to fall apart pretty quickly if you do not have DNS in
place. You can start using host files, but that will get old quickly.
Ideally, the first thing you will do with Puppet is install a DNS server
managed by Puppet. Maybe that will be the next post.

Puppet
======

Starting with a base Centos 6 install, the installation is very easy:

::

    yum -y install https://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm
    yum -y install puppet puppet-server rubygem-activerecord

Our environments need a place to go, so create that:

::

    mkdir /etc/puppet/environments
    chgrp puppet /etc/puppet/environments
    chmod 2775 /etc/puppet/environments

The configuration will look like:

::

    [main]
    logdir = /var/log/puppet
    rundir = /var/run/puppet
    ssldir = $vardir/ssl
    trusted_node_data = true
    pluginsync = true
        
    [agent]
    classfile = $vardir/classes.txt
    localconfig = $vardir/localconfig
    report = true
    environment = production
    ca_server = puppet.chriscowley.lan
    server = puppet.chriscowley.lan
        
    [master]
    environmentpath = $confdir/environments
    # Passenger
    ssl_client_header        = SSL_CLIENT_S_DN
    ssl_client_verify_header = SSL_CLIENT_VERIFY

Do not use the Puppetmaster service. It uses Webrick, which is bad. Any
more than 5 agents and it will start slowing down. Puppet is a RoR app,
so stick it behind
`Apache/Passenger <https://docs.puppetlabs.com/guides/passenger.html>`__.
We installed the ``puppet-server`` package for a simple reason: when you
start it the first time, it will create your SSL certificates
automatically. After that initial start you can stop it and forget it
ever existed. So just run:

::

    service puppetmaster start
    service puppetmaster stop

Unfortunately, you will need to put SELinux into Permissive mode
temporarily. Once you have fired it up you can `build a local
policy <https://wiki.centos.org/HowTos/SELinux#head-faa96b3fdd922004cdb988c1989e56191c257c01>`__
and re-enable it.

::

    yum install httpd httpd-devel mod_ssl ruby-devel rubygems gcc gcc-c++ curl-devel openssl-devel zlib-devel
    gem install rack passenger
    passenger-install-apache2-module

Next you need to configure Apache to serve up the RoR app.

::

    mkdir -p /usr/share/puppet/rack/puppetmasterd
    mkdir /usr/share/puppet/rack/puppetmasterd/public /usr/share/puppet/rack/puppetmasterd/tmp
    cp /usr/share/puppet/ext/rack/config.ru /usr/share/puppet/rack/puppetmasterd/
    chown puppet:puppet /usr/share/puppet/rack/puppetmasterd/config.ru
    https://gist.githubusercontent.com/chriscowley/00e75ee021ce314fab1e/raw/c87abc38182eafc6d22a80d13078ac044fdde49f/puppetmaster.conf | sed 's/puppet-server.example.com/puppet.yourlan.lan/g'

You will need to modify the ``sed`` command in the last line to match
your environment.

You may also need to change the Passenger paths to match what the output
of ``passenger-install-apache2-module`` told you. It is up to date as of
the time of writing.

Hiera
=====

Your config file (``/etc/puppet/hiera.yaml``) will already be created,
mine looks like this:

::

    :backends:
      - yaml
    :hierarchy:
      - defaults
      - "nodes/%{clientcert}"
      - "virtual/%{::virtual}"
      - "%{environment}"
      - "%{::osfamily}"
      - global

    :yaml:
      :datadir: "/etc/puppet/environments/%{::environment}/hieradata"

There is also an ``/etc/hiera.yaml`` which Puppet does not use. change
this to a symbolic link to avoid confusion.

::

    ln -svf /etc/puppet/hiera.yaml /etc/hiera.yaml

If you were to test it now, you will see a few errors:

::

    Info: Retrieving pluginfacts
    Error: /File[/var/lib/puppet/facts.d]: Could not evaluate: Could not retrieve information from environment production source(s) puppet://puppet/pluginfacts
    Info: Retrieving plugin
    Error: /File[/var/lib/puppet/lib]: Could not evaluate: Could not retrieve information from environment production source(s) puppet://puppet/plugins

Don't worry about that for now, the important thing is that the agent
connects to the master. If that happens the master does return an HTTP
error, then you are good.

R10k
====

This is the tool I use to manage my modules. It can pull them off the
Forge, or from wherever you tell it too. Most often that will be Github,
or an internal Git repo if that's what you use.

You need to install it from Ruby Gems, then there is a little
configuration to do.

::


    gem install r10k
    mkdir /var/cache/r10k
    chgrp puppet /var/cache/r10k
    chmod 2775 /var/cache/r10k

The file ``/etc/r10k.yaml`` should contain:

::

    # location for cached repos
    :cachedir: '/var/cache/r10k'

    # git repositories containing environments
    :sources:
      :base:
        remote: '/srv/puppet.git'
        basedir: '/etc/puppet/environments'

    # purge non-existing environments found here
    :purgedirs:
      - '/etc/puppet/environments'

Git
===

The core of your this process is the ubiquitous Git.

::

    yum install git

You need a Git repo to store everything, and also launch a deploy script
when you push to it. To start with we'll put it on the Puppet server. In
the future I would put this on a dedicated machine, have Jenkins run
tests, then run the deploy script on success.

However, it is not a standard repository, so you cannot just run
``git init``. It needs:

-  To be **bare**
-  To be **shared**
-  Have the **master** branch renamed to **production**

::

    mkdir -pv /srv/puppet.git
    git init --bare --shared=group /srv/puppet.git
    chgrp -R puppet /srv/puppet.git
    cd /srv/puppet.git
    git symbolic-ref HEAD refs/heads/production

Continuing to work as root is not acceptable, so create user (if you do
not already have one).

::

    useradd <username>
    usermod -G wheel,puppet <username>
    visudo

Uncomment the line that reads:

::

    %wheel        ALL=(ALL)       ALL

This gives your user full ``sudo`` privileges.

Deploy script
=============

This is what does the magic stuff. It needs to be
``/srv/puppet.git/hooks/post-receive`` so that it runs when you push
something to this repository.

::

    #!/bin/bash

    umask 0002

    while read oldrev newrev ref
    do
        branch=$(echo $ref | cut -d/ -f3)
        echo
        echo "--> Deploying ${branch}..."
        echo
        r10k deploy environment $branch -p
        # sometimes r10k gets permissions wrong too
        find /etc/puppet/environments/$branch/modules -type d -exec chmod 2775 {} \; 2> /dev/null
        find /etc/puppet/environments/$branch/modules -type f -exec chmod 664 {} \; 2> /dev/null
    done

Run ``chmod 0775 /srv/puppet.git/hooks/post-receive`` to make is
executable and writable by anyone in the ``puppet`` group.

The first environment
=====================

Switch to your user

::

    su - <username>

Clone the repository and create the necessary folder structure:

::

    git clone /srv/puppet.git
    cd puppet
    mkdir -pv hieradata/nodes manifests site

Now you can create ``PuppetFile`` in the root of that repository. This
is what tells R10k what modules to deploy.

::

    # Puppet Forge
    mod 'puppetlabs/ntp', '3.0.0-rc1'
    mod 'puppetlabs/puppetdb', '3.0.1'
    mod 'puppetlabs/stdlib', '3.2.1'
    mod 'puppetlabs/concat', '1.0.0'
    mod 'puppetlabs/inifile', '1.0.3'
    mod 'puppetlabs/postgresql', '3.3.3'
    mod 'puppetlabs/firewall', '1.0.2'
    mod 'chriscowley/yumrepos', '0.0.2'

    # Get a module from Github
    #mod 'custom',
    #  :git => 'https://github.com/chriscowley/puppet-pydio.git',
    #  :ref => 'master'

A common error I make if I am not looking properly is to put the SSH URL
from Github in there. This will not work unless you have added your SSH
key on the Puppet server. Better just to put the HTTPS URL in there,
there is need to write back to it after all.

Next you need to tell Puppet what agents should get what. To begin with,
everything will get NTP, but only the Puppetmaster will get PuppetDB. To
that end create ``hieradata/common.yaml`` with this:

::

    classes:
      - ntp

    ntp::servers:
      - 0.pool.ntp.org
      - 1.pool.ntp.org
      - 2.pool.ntp.org
      - 3.pool.ntp.org

Next create ``hieradata/nodes/$(hostname -s).yaml`` with:

::

    classes:
      - puppetdb
      - puppetdb::master::config

Finally, you need to tell Puppet to get the data from Hiera. Create
``manifests.site.pp`` with

::

    hiera_include('classes')

You should need nothing else.

Now you can push it to the master repository.

::

    git add .
    git commit -a -m "Initial commit"
    git branch -m production
    git push origin production

Testing
=======

Of course, the whole point of all this is that we do as much testing as
we can before any sort of deploy. We also want to keep our Git
repository nice clean (especially if you push it to Github), so if we
can avoid commits with stupid errors that would be great.

To perform your testing you need to replicate your production
environment. From now on, I'm going to assume that you are working on
your own workstation.

Clone your repository:

::

    git clone ssh://<username>@puppet.example.com/srv/puppet.git
    cd puppet

To perform all the testing, `RVM <https://rvm.io/>`__ is your friend.
This allows you to replicate the ruby environment on the master, have
all the necessary gems installed in a contained environment and sets you
up to integrate with Jenkins later. Install is with:

::

    curl -sSL https://get.rvm.io | bash -s stable

Follow any instructions it gives your, then you can create your
environment. This will be using a old version of ruby as we are running
CentOS 6 on the master.

::

    rvm install ruby-1.8.7
    rvm use ruby-1.8.7
    rvm gemset create puppet
    rvm gemset use puppet
    rvm --create use ruby-1.8.7-head@puppet --rvmrc

Create a Gemfile that contains:

::

    source 'https://rubygems.org'
     
    gem 'puppet-lint', '0.3.2'
    gem 'puppet', '3.6.2'
    gem 'kwalify', '0.7.2'

Now you can install the gems with ``bundle install``.

The tests will be run by a pre-commit hook script, that looks something
like:

::

    #!/bin/bash
    # pre-commit git hook to check the validity of a puppet main manifest
    #
    # Prerequisites:
    # gem install puppet-lint puppet
    #
    # Install:
    # /path/to/repo/.git/hooks/pre-commit
    #
    # Authors:
    # Chris Cowley <chris@chriscowley.me.uk>

    echo "Checking style"
    for file in `git diff --name-only --cached | grep -E '\.(pp)'`; do
      puppet-lint ${file}
      if [ $? -ne 0 ]; then
        style_bad=1
      else
        echo "Style looks good"
      fi
    done

    echo "Checking syntax"
    for file in `git diff --name-only --cached | grep -E '\.(pp)'`; do
      puppet parser validate $file
      if [ $? -ne 0 ]; then
        syntax_bad=1
        echo "Syntax error in ${file}"
      else
        echo "Syntax looks good"
      fi
    done

    for file in `git diff --name-only --cached | grep -E '\.(yaml)'`; do
      echo "Checking YAML is valid"
      ruby -e "require 'yaml'; YAML.parse(File.open('$file'))"
      if [ $? -ne 0 ]; then
        yaml_bad=1
      else
        echo "YAML looks good"
      fi
    done

    if [ ${yaml_bad}  ];then
      exit 1
    elif [ ${syntax_bad}  ]; then
      exit 1
    elif [ ${style_bad}  ]; then
      exit 1
    else
      exit 0
    fi

This should set you up very nicely. Your environments are completely
dynamic, you have a framework in place for testing.

For now the deployment is with a hook script, but that is not the
ultimate goal. This Git repo needs to be on the Puppet master. You may
well already have a Git server you want to use. TO this end, in a later
post I will be add Jenkins into the mix. As you are running the tests in
an RVM environment, it will be very easy to put into Jenkins. This can
then perform the deployment.
