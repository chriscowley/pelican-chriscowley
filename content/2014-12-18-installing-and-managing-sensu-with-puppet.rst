Installing and Managing Sensu with Puppet
#########################################
:tags: devops

As promised in the `previous
post </blog/2014/11/18/installing-rabbitmq-on-centos-7/>`__, I thought I
would share my Sensu/Puppet config. This is based on the Puppet
infrastucture I decribed
`here </blog/2014/06/25/super-slick-agile-puppet-for-devops/>`__ so
everything goes into Hiera.

.. raw:: html

   <!-- more -->

For reasons best known to me (or my DHCP server) my Sensu host is on
192.168.1.108.

First your ``Puppetfile`` tells R10k to install the Sensu module, plus a
few more:

::

    mod 'nanliu/staging'
    mod 'puppetlabs/rabbitmq'
    mod 'sensu/sensu'

    mod 'redis',
    :git => 'https://github.com/chriscowley/chriscowley-redis.git',
    :commit => '208c01aaf2435839ada26d3f7187ca80517fa2a8

I tend to put my classes and their parameters in Hiera. My
``hieradata/common.yaml`` contains:

::

    ---
    classes:
    - rabbitmq
    - redis
    - sensu
    rabbitmq::port: '5672'
    sensu::install_repo: true
    sensu::purge_config: true
    sensu::rabbitmq_host: 192.168.1.108
    sensu::rabbitmq_password: password
    sensu::rabbitmq_port: 5672
    sensu::rabbitmq_vhost: '/sensu'
    sensu::use_embedded_ruby: true
    sensu::subscriptions:
      - base

This will do all the configuration for all your nodes. More
specifically:

-  tells RabbitMQ to communicate on 5672/TCP
-  Installs Sensu from their own repo
-  All Sensu config will be controlled by Puppet
-  Configures the Sensu client:
-  RabbitMQ host is 192.168.1.108
-  password is ``password``
-  RabbitMQ server is listening on 5672/TCP
-  RabbitMQ vhost is /sensu
-  Run plugins using Ruby embedded with Sensu, not system. This comes
   with the *sensu-plugins* gem which is required by any community
   plugins.
-  Subscribe to the ``base`` set of plugins

Next up, to configure your master, ensure that
``hieradata/nodes/monitor.whatever.com.yaml`` contains:

::

    ---
    classes:
    sensu::server: true
    sensu::api: true

This does not do everything though. All we have done here is install and
enable the Sensu server and API. Unfortunately, I have not really
settled on a good way of getting defined types into Hiera, so now we
jump into ``manifests/site.pp``.

::

    node default inherits basenode {
      package { 'wget':
        ensure => installed,
      }
      package { 'bind-utils':
        ensure => installed,
      }
      file { '/opt/sensu-plugins':
        ensure => directory,
        require => Package['wget']
      }
      staging::deploy { 'sensu-community-plugins.tar.gz':
        source => 'https://github.com/sensu/sensu-community-plugins/archive/master.tar.gz',
        target => '/opt/sensu-plugins',
        require => File['/opt/sensu-plugins'],
      }
      sensu::handler { 'default':
        command => 'mail -s \'sensu alert\' ops@foo.com',
      }
      sensu::check { 'check_cron':
        command => '/opt/sensu-plugins/sensu-community-plugins-master/plugins/processes/check-procs.rb -p crond -C   1',
        handlers => 'default',
        subscribers => 'base',
        require => Staging::Deploy['sensu-community-plugins.tar.gz'],
      }
      sensu::check { 'check_dns':
        command => '/opt/sensu-plugins/sensu-community-plugins-master/plugins/dns/check-dns.rb -d google-public-dns-a.google.com -s 192.168.1.2 -r 8.8.8.8',
        handlers => 'default',
        subscribers => 'base',
        require => Staging::Deploy['sensu-community-plugins.tar.gz'],
      }
      sensu::check { 'check_disk':
        command => '/opt/sensu-plugins/sensu-community-plugins-master/plugins/system/check-disk.rb',
        handlers => 'default',
        subscribers => 'base',
        require => Staging::Deploy['sensu-community-plugins.tar.gz'],
      }
    }

    This actually does quite a lot (halleluiah for CM). Each host will get:

    - Ensures `wget` is installed and that a directory exists to hold the plugins
    - Deploys those plugins, and follows HEAD. Do not do this in production - change the URL to use a particular commit/tag/whatever.
    - Configures a simple handler to email alerts.
    - Finally we configure a few basic plugins
       - check `crond` is running
       - Check name resolution works by looking up Google's public DNS server
       - Check disk space
       
    Finally, the Sensu server needs RabbitMQ configured:

    node 'monitor.whatever.com' inherits default {
      rabbitmq_user { 'sensu':
        admin => false,
        password => 'password',
      }
      rabbitmq_vhost { '/sensu':
        ensure => present,
      }
    }

If you use Puppet agent with its defaults everything should now kind of
pull together over the next hour.

One final stage is to have some way of visualising your Sensu data.
There is a great dashboard called
`Uchiwa <https://github.com/sensu/uchiwa>`__ for that. In the
``monitor.whatever.com`` node in ``manifests/site.pp`` add:

::

      $uchiwa_api_config = [{
        host    => 'monitor.whatever.lan',
        name    => 'Site 1',
        port    => '4567',
        timeout => '5',
      }]

      class { 'uchiwa':
        install_repo        => false,
        sensu_api_endpoints => $uchiwa_api_config,
        user                => 'admin',
        pass                => 'secret',
      }

You could put this anywhere, but the Sensu host is as pretty logical
place to my mind.

I am not 100% happy with this, particularly some of the dependency
(packages and folders) is quite messy. It is fine for now as my lab is
very much centred around CentOS. I do have some projects on the todo
list for which I may use Debian/Ubuntu. As such I will be breaking a lot
of that out into a *localdata* module. I'll post details about how I do
that when I get round to it.
