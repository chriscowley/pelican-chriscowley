---
layout: post
title: "NFS with Puppet and an ENC"
date: 2014-01-24 20:06
comments: true
categories: ['devops','puppet','linux']
---
{% img right http://puppetlabs.com/sites/default/files/PL_logo_horizontal_RGB_0.svg 200 200 %}Ages ago (it seems) I posted a [howto](http://www.chriscowley.me.uk/blog/2013/04/11/using-hiera-with-puppet/) on configure NFS using Puppet and Hiera. I have been using this happily for several months and adding a new share was is as simple as adding a line to a YAML file. I was never completely happy with it though, especially after I decided to deploy [The Foreman](http://www.theforeman.org) in my lab.
<!-- more -->

The reason I was never satisfied is because The Foreman makes a really good ENC. I wanted to use this, so I have modified my module to use an ENC rather than Hiera directly.

OK, first I we need to get the module into a position where it uses parameterized classes. This is actually quite simple. 

My original manifest is [here](http://gitlab.chriscowley.me.uk/puppet/chriscowley-nfs/blob/b5d5fe6eba75379fad37255ceddb55208cbe7208/manifests/server.pp). The key item is the *$exports* variable, which is hiera data. All I did was create a class parameter called *exports* and removed the variable within the class. You can see the new code [here](http://gitlab.chriscowley.me.uk/puppet/chriscowley-nfs/blob/ab9627cf920f3a87986aa7379168572ca3a55f7e/manifests/server.pp). I have also moved the `list_exports` function out into a [seperate file](http://gitlab.chriscowley.me.uk/puppet/chriscowley-nfs/blob/ab9627cf920f3a87986aa7379168572ca3a55f7e/manifests/list_exports.pp). Apparently this makes it more readable, although I am not convinced in this instance.

I also took the chance to update my module a bit so that it was not hard-coded to my own lab network. To that end, it will automatically pull out the IP address and netmask of eth0. You can edit this easily enough using your ENC.

{% codeblock lang:puppet manifests/server.pp  %}
  class nfs::server (
    $exports = [ '/srv/share'],
    $networkallowed = $::network_eth0,
    $netmaskallowed = $::netmask_eth0,
  ) {
    // Code here
  }
{% endcodeblock %}

Next we need a simple ENC to supply the data. An ENC is actually just any script that returns YAML. It has a single parameter, which is the FQDN of the node. I use this:

{% codeblock /usr/local/bin/simple-enc.sh %}
#!/bin/bash
DATADIR="/var/local/enc"
NODE=$1
 
cat "${DATADIR}/${NODE}.yaml"
{% endcodeblock %}

Next you need a YAML file that looks like:

{% codeblock /var/local/enc/nfs.example.lan.yaml %}
---
environment: production
classes:
  nfs::server:
    exports:
      - /srv/share1
      - /srv/share3
    networkallowed: 192.168.0.0
    netmaskallowed: 255.255.255.0
parameters:
{% endcodeblock %}

Finally, you need to enable this on your Puppet master. Add this to `/etc/puppet/puppet.conf`:

{% codeblock  %}
[master]
    node_terminus = exec
    external_nodes = /usr/local/bin/simple-enc.sh
{% endcodeblock %}

Now whenever a node with the FQDN nfs.example.lan syncs with the master it runs `/usr/local/bin/simple-enc.sh nfs.examle.lan.yaml`. This returns the contents of the YAML file above. The layout of it is pretty logical, but I suggest reading Puppetlabs [docs](http://docs.puppetlabs.com/guides/external_nodes.html).

How is this better than the previous Hiera setup? First I can now use my module with The Foreman which answers my immediate need. Second I can now submit this module to the Forge with a warm fuzzy feeling inside as I am a good citizen. not only does it work with Puppet 3, but also really old versions of Puppet that do not support an ENC or Hiera. It can do this because the user can still edit the class parameters directly, or set the in `site.pp` (**DON'T DO THAT**).

You can install the module on your own Puppet master with:

```
git clone http://gitlab.chriscowley.me.uk/puppet/chriscowley-nfs.git \
    /etc/puppet/modules/nfs/
```
