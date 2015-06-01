Send mail from Gitlab through Mandrill using Postfix
####################################################

:slug: send-mail-from-gitlab-through-mandrill-using-postfix
:data: 2015-06-01
:tags: linux, postfix

.. figure:: http://i.imgur.com/W709cC9m.png
    :align: right
    :alt: gitlab logo

I am a fan of Gitlab. While Github is great, and I `use it heavily <https://github.com/chriscowley>`_, one should never be 100% reliant on the whims of a for-profit company. After all, their agenda is not the same as mine and could chang in the future. I also use it for projects at work where we do not necessarily want to allow public access.

Sending emails however is a little complicated. A good email server needs DNS and and SMTP properly configured. You then spend all your waking hours ensuring that you are not on any blacklists. Once you have done that you may even have to time to do the rest of your job.

Mandrill_ takes care of all this for you, then provides both SMTP and REST access. Gitlab, by default, uses SMTP to send its emails, so you simply configure your SMTP server of choice to use Mandrill to relay its messages. Personally I use Postfix as it is installed by default on RHEL/CentOS. 

In Gitlab, there is nothing to do on a default install. It will use whatever your servers install MTA is. This actually means that this post is actually in no way related to Gitlab - Postfix/Mandrill only.

You will need to install ``cyrus-sasl-plain``:

::

    sudo yum install cyrus-sasl-plain`
    
Modify the file `/etc/postfix/main.cf` to contain:

::

    myorigin = example.com
    smtp_sasl_auth_enable = yes
    smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
    smtp_sasl_security_options = noanonymous
    smtp_use_tls = yes
    relayhost = [smtp.mandrillapp.com]

Next you need to get the credentials Postfix will use to connect to Mandrill. Go into "Settings" -> "SMTP & API Info". Create a new API key for Gitlab. You account name is your username, and this API key will be your password. You can use any API key or a single API key for many services, but I use a separate key for each service. That way, if a service is compromised, I can just delete the key to block it.

.. figure:: http://i.imgur.com/GYvvKrx.png
    :align: center
    :alt: Mandrill settings
    :width: 400px

Create the file ``/etc/postfix/sasl_passwd`` containing:
    
::

    [smtp.mandrillapp.com] <your-account-name>:<a-long-key>
    
You need to secure that, so run ``chmod 600 /etc/postfix/sasl_passwd``.

Finally, you need to map that file and restart Postfix:

::

    sudo /etc/postfix/sasl_passwd
    sudo systemctl restart postfix
    
Voila, now you should be able to send emails from the CLI and Gitlab.
    
.. _Mandrill: https://mandrillapp.com/
