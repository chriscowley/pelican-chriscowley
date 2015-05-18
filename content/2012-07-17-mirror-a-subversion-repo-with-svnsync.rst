Mirror a Subversion repo with svnsync
#####################################
:tags:  Subversion

The basic idea is that everytime a change happens on the master, it gets
pushed to the slave. In this set up it will *not* get you any more
capacity; you cannot commit back to the slave. If you do it will get out
of sync, resulting in a *split brain* situation. This is what we
sysadmins call a "bad thing". I am doing this in order to have Atlassian
Fisheye can scan the repository without having to go over the network.
The basic layout is:

{% img center /images/svnsync.png %}

First the master needs to be able to send the data to the slave without
any user interaction. On both the slave create a user to perform the
sync:

::

    useradd svnsync

On the master, I use https to access my repositories. This means that
all my hook scripts run as the apache user. Change to that user with
``sudo su -s /bin/bash - apache``

Create an ssh key-pair (``ssh-keygen``) and add the contents of
``~apache\.ssh\id_rsa.pub`` on the master to
``~svnsync/.ssh/authorized_keys2`` on the slave.

Now you can push push data to the slave without a password. Test it by
running:

::

    ssh svnsync@<slave>

On Slave
--------

Create a new repository to store what gets pushed to it

::

    svnadmin create --fs-type=fsfs /var/local/svnsync/<reponame>
    chown -Rv svnsync:svnsync /var/local/svnsync/<reponame>

The process will need to make modifications to the properties, so you
need to enable that. Put the following into
``/var/local/svnsync/<reponame>/hooks/pre-revprop-change``

::

    #!/bin/sh
    USER="$3"

    if [ "$USER" = "svnsync" ]; then exit 0; fi

    echo "Only the svnsync user can change revprops" >&2
    exit 1

Finally make it executable with

::

    chmod +x /var/local/svnsync/<reponame>/hooks/pre-revprop-change

On Master
---------

First initialize the transfer and do the initial population. Do all this
as the apache user again.

::

    svnsync init --username svnsync \
        svn+ssh://svnsync@<slave>/var/local/svnsync/<reponame> \
        file:///var/svn/<reponame>

Now we need to configure the Master repo to push all changes to the
slave. Create a post-commit hook script containing

::

    #!/bin/bash
    svnsync --username svnsync --non-interactive sync \
        svn+ssh://svnsync@<slave>/var/local/svnsync/<reponame>

Finally create another hook script to keep revision properties in sync
in ``/var/svn/<reponame>/hooks/post-revprop-change``

::

    #!/bin/bash
    REPOS="$1"
    REV="$2"
    USER="$3"
    PROPNAME="$4"
    ACTION="$5"

    svnsync --username svnsync --non-interactive copy-revprops \
        svn+ssh://svnsync@<slave>/var/local/svnsync/<reponame> $REV && \
        exit 0

