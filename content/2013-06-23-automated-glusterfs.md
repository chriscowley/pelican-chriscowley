---
layout: post
title: "Automated GlusterFS"
date: 2013-06-23 22:02
comments: true
categories: [storage, puppet, devops]
---
{% img right http://www.hastexo.com/system/files/imagecache/sidebar/20120221105324808-f2df3ea3e3aeab8_250_0.png %} As I promised on Twitter, this is how I automate a GlusterFS deployment. I'm making a few assumptions here: 
<!-- more -->

* I am using CentOS 6, so should work on RHEL 6 and Scientific Linux 6 too. Others may work, but YMMV.
   * As I use XFS, RHEL users will need the _Scalable Storage_ option. Ext4 will work, but XFS is recommended.
* That you have a way of automating your base OS installation. My personal preference is to use [Razor](https://github.com/puppetlabs/Razor).
* You have a system with at least a complete spare disk dedicated to a GlusterFS brick. That is the best way to run GlusterFS anyway.
* You have 2 nodes and want to replicate the data
* You have a simple setup with only a single network, because I am being lazy. As a proof-of concept this is fine. Modifying this for second network is quite easy, just change the IP address in you use.

{% img https://docs.google.com/drawings/d/1XA7GH3a4BL1uszFXrSsZjysi59Iinh-0RmhqdDbt7QQ/pub?w=673&h=315 'simple gluster architecture' %}
 
The diagram above shows the basic layout of what to start from in terms of hardware. In terms of software, you just need a basic CentOS 6 install and to have Puppet working.

I use a pair of Puppet modules (both in the Forge): [thias/glusterfs](http://forge.puppetlabs.com/thias/glusterfs) and [puppetlabs/lvm](http://forge.puppetlabs.com/puppetlabs/lvm). The GlusterFS module CAN do the LVM config, but that strikes me as not the best idea. The UNIX philosophy of "do one job well"  holds up for Puppet modules as well. You will also need my [yumrepos](https://github.com/chriscowley/puppet-yumrepos) module.

Clone those 3 modules into your modules directory:

```
cd /etc/puppet/
git clone git://github.com/chriscowley/puppet-yumrepos.git modules/yumrepos
puppet module install puppetlabs/lvm --version 0.1.2
puppet module install thias/glusterfs --version 0.0.3
```

I have specified the versions as that is what was the latest at the time of writing. You should be able to take the latest as well, but comment with any differences if any. That gives the core of what you need so you can now move on to you `nodes.pp`.

```
class basenode {
  class { 'yumrepos': }
  class { 'yumrepos::epel': }
}

class glusternode {
  class { 'basenode': }
  class { 'yumrepos::gluster': }
  
  volume_group { "vg0":
    ensure => present,
    physical_volumes => "/dev/sdb",
    require => Physical_volume["/dev/sdb"]
  }
  physical_volume { "/dev/sdb":
    ensure => present
  }
  logical_volume { "gv0":
    ensure => present,
    require => Volume_group['vg0'],
    volume_group => "vg0",
    size => "7G",
  }
  file { [ '/export', '/export/gv0']:
    seltype => 'usr_t',
    ensure => directory,
  }
  package { 'xfsprogs': ensure => installed
  }
  filesystem { "/dev/vg0/gv0":
    ensure => present,
    fs_type => "xfs",
    options => "-i size=512",
    require => [Package['xfsprogs'], Logical_volume['gv0'] ],
  }
  
  mount { '/export/gv0':
    device => '/dev/vg0/gv0',
    fstype => 'xfs',
    options => 'defaults',
    ensure => mounted,
    require => [ Filesystem['/dev/vg0/gv0'], File['/export/gv0'] ],
  }
  class { 'glusterfs::server':
    peers => $::hostname ? {
      'gluster1' => '192.168.1.38', # Note these are the IPs of the other nodes
      'gluster2' => '192.168.1.84',
    },
  }
  glusterfs::volume { 'gv0':
    create_options => 'replica 2 192.168.1.38:/export/gv0 192.168.1.84:/export/gv0',
    require => Mount['/export/gv0'],
  }
}

node 'gluster1' {
  include glusternode
  file { '/var/www': ensure => directory }
  glusterfs::mount { '/var/www':
    device => $::hostname ? {
      'gluster1' => '192.168.1.84:/gv0',
    }
  }
}

node 'gluster2' {
  include glusternode
  file { '/var/www': ensure => directory }
  glusterfs::mount { '/var/www':
    device => $::hostname ? {
      'gluster2' => '192.168.1.38:/gv0',
    }
  }
}
```

What does all that do? Starting from the top:

   * The `basenode` class does all your basic configuration across all your hosts. Mine actually does a lot more, but these are the relevant parts.
   * The `glusternode` class is shared between all your GlusterFS nodes. This is where all your Server configuration is.
   * Configures LVM
      * Defines the Volume Group "vg0" with the Physical Volume `/dev/sdb`
      * Creates a Logical Volume "gv0" for GlusterFS use and make it 7GB
   * Configures the file system
      * Creates the directory `/export/gv0`
      * Formats the LV created previously with XFS (installs the package if necessary)
      * Mounts the LV at `/export/gv0`
      
This is now all ready for the GlusterFS module to do its stuff. All this happens in those last two sections.

   * The class `glusterfs::Server` sets up the peering between the two hosts. This will actually generate a errors, but do not worry. This because gluster1 successfully peers with gluster2. As a result gluster2 fails to peer with gluster1 as they are already peered.
   * Now `glusterfs::volume` creates a replicated volume, having first ensured that the LV is mounted correctly.
   * All this is then included in the node declarations for `gluster1` and `gluster2`.
   
All that creates the server very nicely. It will need a few passes to get everything in place, while giving a few red herring errors. It should would however, all the errors are there in the README for the GlusterFS module in PuppetForge, so do not panic.

A multi-petabyte scale-out storage system is pretty useless if the data cannot be read by anything. So lets use those nodes and mount the volume. This could also be a separate node (but once again I am being lazy) the process will be exactly the same.

   * Create a mount point for it ( `file {'/var/www': ensure => directory }
   * Define your `glusterfs::mount` using any of the hosts in the cluster.
   
Voila, that should all pull together and give you a fully automated GlusterFS set up. The sort of scale that GlusterFS can reach makes this sort of automation absolutely essential in my opinion. This should be relatively easy to convert to Chef or Ansible, whatever takes your fancy. I have just used Puppet because of my familiarity with it.

This is only one way of doing this, and I make no claims to being the most adept Puppet user in the world. All I hope to achieve is that someone finds this useful. Courteous comments welcome.
