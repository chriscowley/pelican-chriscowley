title: "Installing RabbitMQ on CentOS 7"
date: 2014-11-18 20:39
comments: true
Very quick as I did not find any good solutions to this on Google. This is actually an interim post as I ran across this while configuring [Sensu](https://sensuapp.org/) in my lab. A full post on that, along with configuring it with [my Puppet set up](https://www.chriscowley.me.uk/blog/2014/06/25/super-slick-agile-puppet-for-devops/) is coming.
<!-- more -->

RabbitMQ is in EPEL (slightly old, but not drastically) so install that first, then install from `yum`.

```
yum -y install https://mirrors.ircam.fr/pub/fedora/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
yum -y install rabbitmq-server
```

Well that was easy, so just start it with

```
systemctl rabbitmq-server start
```

And it starts

...


except it does not :-(

In fact it is blocked by 2 things:

- Firewall
- SELinux

I found an answer on [StackOverflow](https://stackoverflow.com/questions/25816918/not-able-to-start-rabbitmq-server-in-centos-7-using-systemctl) which was basically "Turn it all off". This is quite frankly an answer for the weak! How about actually solving the problem people!

```
firewall-cmd --permanent --add-port=5672/tcp
firewall-cmd --reload
setsebool -P nis_enabled 1
```

Now you can start the service and enable it:

```
systemctl enable rabbitmq-server
systemctl start rabbitmq-server
```


