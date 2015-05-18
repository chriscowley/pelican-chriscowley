SFTP Chroot on CentOS
#####################
:tags:  linux

This came up today where I needed to give secure file transfer to
customers. To complicate things I had to use an out-of-the-box RHEL6
system. The obvious answer was to use SSH and limit those users to SFTP
only. Locking them into a chroot was not a requirement, but it seemed
like a good idea to me. I found plenty of docs that got 80% of the way,
or took a shortcut, but this should be complete.

The basic steps are:

1. Create a group and the users to that group
2. Modify the SSH daemon configuration to limit a group to sftp only
3. Setup file system permissions
4. Configure SELinux
5. Test (of course)

Without further ado, lets get started. It should only take about 10
minutes, nothing here is especially complex.

Create a group that is limited to SFTP only and a user to be in that
group.

::

    groupadd sftponly
    useradd sftptest
    usermod -aG sftponly  sftptest

Now you need to make a little change to ``/etc/ssh/sshd_config``. There
will be a *Subsystem* line for ``sftp`` which you need to change to
read:

::

    Subsystem       sftp    internal-sftp

Now you need to create a block at the end to limit members of a group
(ie the sftponly group you created above) and chroot them. Simply add
the following to the end of the file:

::

    Match Group sftponly
        ChrootDirectory %h
        ForceCommand internal-sftp
        X11Forwarding no
        AllowTcpForwarding no

These changes will require a reload of the SSH daemon:
``service sshd reload``

Now you need to make some file permission changes. For some reason which
I cannot work out for now, the home directory must be owned by root and
have the permissions 755. So we will also need to make a folder in the
home directory to upload to and make that owned by the user.

::

    sudo -u sftptest mkdir -pv /home/sftptest/upload
    chown root. /home/sftptest
    chmod 755 /home/sftptest
    chgrp -R sftponly /home/sftptest

The last thing we need to do is tell SELinux that we want to upload
files via SFTP to a chroot as it is read-only by default. Of course you
are running SELinux in enforcing mode aren't you :)

::

    setsebool -P ssh_chroot_rw_homedirs on

Now from another console you can sftp to your server

::

    sftp sftptest@<server>

You should then be able to put a file in your upload folder. However if
you try to ssh to the server as the user *sftptest* it should tell you
to go away. Of course you should be able to *ssh* as your normal user
with no problem. Pro tip: make sure to leave a root terminal open just
in case.

Required reading:

-  `CentOS Wiki SELinux <https://wiki.centos.org/HowTos/SELinux>`__
-  `CentOS Wiki
   SELinuxBooleans <https://wiki.centos.org/TipsAndTricks/SelinuxBooleans>`__

