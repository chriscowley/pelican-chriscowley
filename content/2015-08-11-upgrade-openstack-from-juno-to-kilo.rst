Upgrade Openstack from Juno to Kilo
###################################

:slug: upgrade-openstack-from-juno-to-kilo
:date: 2015-08-11
:category:
:tags: openstack, linux

.. figure:: http://i.imgur.com/UAyzTqf.gif
    :align: right
    :alt: Openstack logo
    
It's a process that strikes fear into the hearts of Sysadmins everywhere. This weekend I finally got round to upgrading the Openstack cluster in my lab to Kilo. As I have no spare machines lying around (Intel NUC/HP Microserver/similar donations welcome) I did it in place.

Did it go well? Mostly...

My base was a Juno install from Packstack. If your Juno install was different, then YMMV, but the idea should transfer. The basic process was to install the Kilo yum repo, then run an upgrade:

::

    sudo yum install http://rdo.fedorapeople.org/openstack-kilo/rdo-release-kilo.rpm
    sudo yum upgrade
    
Then a reboot. Finshed...

No, nothing is ever that simple.

In fact most of the services fail dismally due to DB schema updates. This is relatively easily fixed though

Keystone
========

::

    systemctl stop httpd openstack-keystone.service
    systemctl disable openstack-keystone.service
    sudo -u keystone keystone-manage db_sync

The application itself was not updated by the packages, so I collected the lated code from Github:

::

    curl http://git.openstack.org/cgit/openstack/keystone/plain/httpd/keystone.py?h=stable/kilo  \
      | sudo tee /var/www/cgi-bin/keystone/main /var/www/cgi-bin/keystone/admin

Ensure that to Apache config files are as the should be.

``/etc/httpd/conf.d/10-keystone_wsgi_admin.conf``:

::

    <VirtualHost *:35357>
      ServerName keystone.example.com
      WSGIDaemonProcess keystone_admin processes=5 threads=1 user=keystone group=keystone
      WSGIProcessGroup keystone_admin
      WSGIScriptAlias / /var/www/cgi-bin/keystone/admin
      WSGIPassAuthorization On
      LogLevel info
      ErrorLogFormat "%{cu}t %M"
      ErrorLog /var/log/httpd/keystone-error.log
      CustomLog /var/log/httpd/keystone-access.log combined
    </VirtualHost>

and ``/etc/httpd/conf.d/10-keystone_wsgi_main.conf``:

::

    <VirtualHost *:5000>
      ServerName keystone.example.com
      WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
      WSGIProcessGroup keystone-public
      WSGIScriptAlias / /var/www/cgi-bin/keystone/main
      WSGIApplicationGroup %{GLOBAL}
      WSGIPassAuthorization On
      LogLevel info
      ErrorLogFormat "%{cu}t %M"
      ErrorLog /var/log/httpd/keystone-error.log
      CustomLog /var/log/httpd/keystone-access.log combined
    </VirtualHost>


Now restart Apache:

::

    systemctl start httpd.service
    
Glance
======

There was nothing surprising here really. Stop the services, update the database and restart the services.

::

    sudo systemctl stop openstack-glance-api.service openstack-glance-registry.service
    sudo -u glance glance-manage db_sync
    sudo systemctl start openstack-glance-api.service openstack-glance-registry.service
        
Nova
====

Again Nova was quite simple. Stop services, update DB and start again.

::

    sudo systemctl stop openstack-nova-api.service \
      openstack-nova-cert.service openstack-nova-compute.service \
      openstack-nova.compute.service openstack-nova-conductor.service \
      openstack-nova-consoleauth.service openstack-nova-network.service \
      openstack-nova-novncproxy.service openstack-nova-objectstore.service \
      openstack-nova-scheduler.service openstack-nova-volume.service
    sudo -u nova nova-manage db null_instance_uuid_scan
    sudo -u nova "nova-manage db sync
    sudo systemctl start openstack-nova-api.service \
      openstack-nova-cert.service openstack-nova-compute.service \
      openstack-nova.compute.service openstack-nova-conductor.service \
      openstack-nova-consoleauth.service openstack-nova-network.service \
      openstack-nova-novncproxy.service openstack-nova-objectstore.service \
      openstack-nova-scheduler.service openstack-nova-volume.service

Neutron
=======

This need a few tweaks in ``/etc/neutron/neutron.conf``.

In the [DEFAULT] section, change the value of the rpc_backend option:  ``neutron.openstack.common.rpc.impl_kombu`` becomes ``rabbit``

In the [DEFAULT] section, change the value of the core_plugin option: ``neutron.plugins.ml2.plugin.Ml2Plugin`` becomes ``ml2``

In the [DEFAULT] section, change the value or values of the service_plugins option to use short names. For example: ``neutron.services.l3_router.l3_router_plugin.L3RouterPlugin`` becomes ``router``

In the [DEFAULT] section, explicitly define a value for the ``nova_region_name`` option. For example:
        	
::

    [DEFAULT]
    ...
    nova_region_name = regionOne
    
Stop the services and upgrade the DB:

::

    sudo systemctl stop neutron-dhcp-agent.service neutron-l3-agent.service \
      neutron-metadata-agent.service neutron-openvswitch-agent.service \
      neutron-ovs-cleanup.service neutron-server.service
    sudo -u neutron neutron-db-manage --config-file /etc/neutron/neutron.conf \
      --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade kilo
      
Now you can restart Neutron

::

    sudo systemctl start neutron-dhcp-agent.service neutron-l3-agent.service \
      neutron-metadata-agent.service neutron-openvswitch-agent.service \
      neutron-ovs-cleanup.service neutron-server.service

Horizon
=======

This pretty much worked, but what I did see is that once mu login ticket expired then I could not login unless I cleared the cookie out.

This is easily fixed by adding ``AUTH_USER_MODEL = 'openstack_auth.User'`` to ``/etc/openstack-dashboard/local_settings``.

Cinder
======

This is what gave me the most problems. Basically, the database for Cinder itself, the database for Nova volumes and the actual iSCSI target got out of sync. I ran ``nova volume-detach ...`` and it got stuck in a detaching state.

Basically, I had to go through and get it into a know state (volumes attached to anything) via the back door.

As an admin, force the volume into "available" with:

::

    nova volume-detach <instance_uuid> <volume_id>
    cinder reset-state --state available <volume_id>
    
Using `targetcli`__ ensure that there are no ACLs on the LUNs. They will be named with the volume_id. I'll not go into the details of how to use ``targetcli``, just that you remove a *file* from the virtual tree that it creates.

Next up you'll need to going to manipulate the Cinder database (hope you still have your packstack file). Standard disclaimer: You can royally screw things up here, so tread carefully, use transactions and take a backup first.

::

    update cinder.volumes set attach_status='detached',
        status='available' where id ='$volume_id';

Now do the same in Nova.

::

    delete from block_device_mapping where not deleted
        and volume_id='$volume_id'
    
You should now be able re-attach the volume to the instance using the CLI. However, I had one that persisted in playing silly buggers. I had to manually update the Cinder DB that is in the *attached* state:

::

    update cinder.volumes set attach_status='attached',
        status='in-use' where id ='$volume_id';

Finally do a full reboot to ensure that everything comes back as you expect.

I am pretty sure that is everything.

Conclusion
==========

I think this was the first time I have done an upgrade of Openstack in place. Considering the fear that this operation puts in people, I think it went pretty smoothly.

I started the install Friday evening, the upgrade was finished that night. Most of my lab instances were up and running by Saturday evening (having spent the day at the beach). All bar one were running Sunday evening (after another trip to the beach). The last instance (with the awkward Cinder volume) was running this morning (again, wait for it: after a trip to the beach yesterday).

__ http://linux-iscsi.org/wiki/Targetcli#Quick_start_guide
