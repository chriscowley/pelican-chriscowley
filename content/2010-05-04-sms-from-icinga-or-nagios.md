Title: SMS from Icinga or Nagios
comments: true
categories: monitoring

Finding out how to have Nagios (or in my case Icinga) send SMS alerts is easy. However, from my point of view it fell down in 2 ways.

1. Most of these guides are Debian specific, I am using Centos.
1. The SMS alerts are all or nothing, I only want SMS alerts for specific services (such as the corporate website).
<!-- more -->

## Hardware

First things first you need something to send the SMS. I am using a brand new Vodaphone USB dongle taped to the side of the rack . I also had it working with a Nokia E51 using the same tools – obviously this would the require constant charging.

Ideally I would have prefered to use an internal card. PCI -> PC card bridges do exist, but I had no joy on my Icinga server, although it did work in a Dell Optiplex we had lying around, but it caused an HP XW4600 not to switch on at all.

## Software

I am using <a href="http://smstools3.kekekasvi.com/" target="_blank">SMS Server Tools 3</a> which are available for Centos/RHEL in <a href="https://fedoraproject.org/wiki/EPEL" target="_blank">EPEL</a>. This gives you an smsd daemon that watches a folder for text messages in a particular format.

When you have enabled EPEL run
```
yum install smstools
chkconfig –levels 35 smsd on
```

When I plugged in the USB dongle I got a pair of USB ttys at /dev/ttyUSB0 and /dev/ttyUSB1

Add the following to /etc/smsd.conf
```
devices = GSM1
logfile = /var/log/smsd.log
loglevel = 7

ARVE Error: no video ID
device = /dev/ttyUSB0
smsc = 447785016005 # I am using Vodaphone, your’s may vary.
incoming = no
```
Now you can start the daemon

    /etc/init.d/smsd start

Finally, for reasons explained later, you need an entry in icinga’s cron.
```
* * * * * if [[ `ls /tmp/ | grep 'sms-icinga' | wc -l` -gt 0 ]];then /bin/mv /tmp/sms-icinga* /var/spool/sms/outgoing/;fi
```

What does this do? It checks “/tmp/” for any files that contain the name “sms-icinga” every minute. If any exist it moves them to “/var/spool/sms/outgoing/”. That last folder is watched by smsd for those special text files mentioned above.
Icinga/Nagios configuration

First add the commands, for which I use the file /etc/icinga/objects/commands.conf
```
define command {
    command_name notify-host-by-sms
    command_line /usr/bin/printf “%b” “To: $CONTACTPAGER$\n\n$NOTIFICATIONTYPE$\nHost Alert: $HOSTNAME$ is $HOSTSTATE$\n” > /tmp/sms-icinga.$HOSTNAME$.$HOSTSTATE$.$CONTACTPAGER$
}

define command {
    command_name notify-service-by-sms
    command_line /usr/bin/printf “%b” “To: $CONTACTPAGER$\n\n$NOTIFICATIONTYPE$\nService Alert:     $SERVICEDESC$ on $HOSTNAME$ is $SERVICESTATE$” > /tmp/sms-icinga.$SERVICEDESC$.$HOSTNAME$.$CONTACTPAGER$
}
```
These commands write a file in /tmp that includes the string sms-icinga that our cron script looks for. The rest of it is to endure we do not accidentally overwrite an alert that has not been sent yet. The reason we need to write it into tmp, and the mv it to the outgoing folder is a little weird. I found that if I wrote directly to the outgoing folder, then smsd seemed picked it up too early and failed to parse the file correctly – strange, but not to worry.

Now is where need to fiddle things a little bit if we only want to send messages for certain critical services. If you want SMS alerts for all your services you can just add a pager entry to all you contacts. We need to create an SMS user and a couple of templates to base our critical stuff on.

The templates:
```
define contact {
    name sms-contact
    use generic-contact
    service_notification_commands notify-service-by-sms, notify-service-by-email
    host_notification_commands notify-host-by-sms, notify-host-by-email
    register 0
}

define service {
    use generic-service
    name critical-service
    contact_groups admins-sms,linux-admin
}

define host {
    name critical-host
    use generic-host
    contact_groups admins-sms,linux-admin
}
```
my user:
```
define contact {
    contact_name ChrisCowley-SMS
    use sms-contact
    pager <my-mobile-number>
}
```
a contact group:
```
define contactgroup {
    contactgroup_name admins-sms
    members ChrisCowley-SMS
}
```

Finally we can create our essential service:

```
define service {
    use critical-service
    service_description Website-content
    check_command check_http_content!-U http://www.snellgroup.com -m Snell
    host_name www.snellgroup.com
}
```

