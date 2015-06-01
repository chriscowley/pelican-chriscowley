Identify and mounting Cinder Volumes in Openstack Heat
######################################################
:tags: openstack

I'm back playing with Openstack again. The day job once again Openstack
based, and as of last week my lab is all Openstack too. While
`oVirt <http://ovirt.org>`__ is awesome, I felt like a change.

Anyway, the meat of today's problem comes from the day job. I have some
instances deployed via heat that have multiple Cinder volumes attached
to them, these then need to be mounted in a certain way. The syntax for
attaching a cinder volume to an instance is:

::

    instance_vol_att:
        type: OS::Cinder::VolumeAttachment
        properties:
          instance_uuid:  { get_resource: instance }
          volume_id: { get_resource: instance_vol_data }
          mountpoint: /dev/vdb

See at the end there is ``mountpoint``? Awesome, my device will always
appear as /dev/vdb!

No! Unfortunately, there is no link between Cinder/Nova and *udev*
within the instance. As a result, udev will simply assign it a device
name in the same way your workstation does to a USB key: it could be
anything.

So what is a poor Openstack admin to do?

Each volume has a UUID, which in the example above. Lets start with a
simple HOT template to create a single instance and volume:

::

    heat_template_version: 2014-10-16
    description: A simple server to run Jenkins

    parameters:
      imageid:
        type: string
        default: Centos-7-x64
        description: Image use to boot a server

    resources:
      jenkins:
        type: OS::Nova::Server
        properties:
          image: { get_param: ImageID }
          flavor: m1.tiny
          networks:
          - network: { get_param: NetID }
      jenkins_data:
        type: OS::Cinder::Volume
        properties:
          size: 50G
      jenkins_data_att:
        type: OS::Cinder::VolumeAttachment
        properties:
          instance_uuid: { get_resource: jenkins }
          volume_id: { get_resource: jenkins_data}

That will create everything we need. The rest we need to pass though
from Nova to the instance somehow. While Nova does not talk to udev, it
does pass the ``volume_id`` though, albeit with a caveat. the ID is
truncated to **20** characters and is available as
``/dev/disk/by-id/virtio-volid20chars``. We can now access this using
the userdata property and ``cloud-init``.

I actually create a small bash script then run it later, so now my
*Server* resource will look like:

::

    jenkins:
      type: OS::Nova::Server
        properties:
          image: { get_param: ImageID }
          flavor: m1.tiny
          networks:
            - network: { get_param: NetID }
          user_data_format: RAW
          user_data:
            str_replace:
              template: |
                #cloud-config
                write_files:
                  - content: |
                      #!/bin/bash
                      voldata_id="%voldata_id%"
                      voldata_dev="/dev/disk/by-id/virtio-$(echo ${voldata_id} | cut -c -20)"
                      mkfs.ext4 ${voldata_dev}               
                      mkdir -pv /var/lib/jenkins
                      echo "${voldata_dev} /var/lib/jenkins ext4 defaults 1 2" >> /etc/fstab
                      mount /var/lib/jenkins
                    path: /tmp/format-disks
                    permissions: '0700'
                runcmd:
                  - /tmp/format-disks
              params:
                "%voldata_id%": { get_resource: jenkins_data }
    jenkins_data:
      type: OS::Cinder::Volume
      properties:
        size: 50
    jenkins_data_att:
      type: OS::Cinder::VolumeAttachment
      properties:
        instance_uuid: { get_resource: jenkins }
        volume_id: { get_resource: jenkins_data}

What is happenning here? I create 3 resources:

-  a server
-  a volume
-  a volume attachment

Within the server there is a *cloud-init* script passed in via
*user*\ data\_. This cloud-init script is created using a template which
has a single parameter. This parameter is ``%voldata_id%`` - I put ``%``
symbols around all my variables in this context, it makes false matches
pretty much impossible. The ``get_resource`` command collects the ID of
the Cinder volume I created.

Now we move into the *cloud-init* script created which does 2 things:

-  creates a bash script, including the variable for the ID
-  launches that scripts

The Bash script calculates what the device will be (``$voldata_dev``),
formats it and mounts it at the mountpoint it creates. It also adds this
into ``/etc/fstab`` for the future.

This can easily be used for multiple volumes. All one does is add an
extra parameter to collect the extra resources, then extend the Bash
script to do them too.
