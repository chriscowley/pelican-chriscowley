title: "Using Hiera with Puppet"
date: 2013-04-11 20:24
comments: true
Using Hiera with Puppet is something I have struggled with a bit. I could see the benefits, namely decoupling my site configuration from my logic. However, for some reason I struggled a bit to really get my head around it. This was compounded by it being quite new (only really integrated in Puppet 3), so the docs are  little lacking.
<!-- more -->

There is some though, the [documentation on PuppetLab's site](https://docs.puppetlabs.com/hiera/latest/) is excellent, but a bit light. It explains the principles well, but is a little limited in real-world examples. Probably the best resource I found was Kelsey Hightower's excellent presentation at [PuppetConf 2012](https://youtu.be/z9TK-gUNFHk):

I learnt a lot from that, but it would be nice if there was an equivalent written down. I suppose that is what I am aiming at here.

# Configuration

  * [NFS Module](https://github.com/chriscowley/puppet-nfs)
  * [Hiera Config](https://github.com/chriscowley/my-master-puppet/blob/master/hiera.yaml)
  * [Hiera Data](https://github.com/chriscowley/my-master-puppet/tree/master/hieradata)


I am using Open Source Puppet 3. If you are using 2.7 or Puppet Enterprise, files will be in a slightly different place. That is all explained in the documentation linked above.

The first thing you need to do is configure Hiera using the file `/etc/puppet/hiera.yaml`. Mine looks like this:

```
:backends:
- yaml
:yaml:
:datadir: /etc/puppet/hieradata/
:hierarchy:
- %{::clientcert}
- common
```

This tells Hiera to use only the YAML backend - I do not like JSON because it always looks messy to me. It will look for the data in the folder `/etc/puppet/hieradata`. Finally it will look in that folder for a file called <clientcert>.yaml, then common.yaml. The process it uses to apply the values is explained very nicely in this image:
{% img https://docs.puppetlabs.com/hiera/latest/images/hierarchy1.png %}

Next, create the file `/etc/puppet/hieradata/<certname>.yaml` that contains your NFS exports:

```
exports:
- /srv/iso
- /srv/images
```

Now, checkout my NFS module from Github links above. If you are not on RHEL6 or similar (I use Centos personally) you will have to modify it as needed.

There are 2 files that are really interesting here. The manifest file (manifests/server.pp) and the template to build the `/etc/exports` file (templates/exports.erb). We'll take apart the manifest, the template just iterates over the data passed to it from that.

The first line creates an array variable called $exports from the Hiera data. Specifically, it looks for a key called _exports_. Hiera then goes through the hierarchy explained earlier looking for that key. In this case it will find it in the <certname>.yaml.

This data is now used for 2 things. First it creates the necessary folders, then it build `/etc/exports`. Here there is a minor problem, because you cannot do a _for each_ loop in a Puppet manifest. We can fiddle it a bit by using a [defined type](https://docs.puppetlabs.com/puppet/3/reference/lang_defined_types.html).

The line `list_exports { $exports:; }` passes the `$exports` array to the type we define above it. This then goes ahead and creates the folders ready to be exported. The `->` builds an [order relationship](https://docs.puppetlabs.com/puppet/3/reference/lang_relationships.html#chaining-arrows) with the File resource for _/etc/exports_. Specifically, that the directories need to be created before they are exported.

```
  define list_exports {
    $export = $name
    file { $export:
      ensure => directory,
      mode => '0755',
      owner => 'root',
      group => 'root'
    }
  }
  list_exports { $exports:; } -> File['/etc/exports']
```

Now it can go ahead and build the `/etc/exports` file using that same $exports array in the `templates/exports.erb` template:

```
  <% [exports].flatten.each do |export| -%>
  <%= export %> 192.168.1.0/255.255.255.0(rw,no_root_squash,no_subtree_check)
  <% end -%>
```
  
There is nothing especially Hiera'y about this, other than where the data in that array came from.

The rest of the manifest deals with installing the packages and configuring services. Once again, nothing especially linked with Hiera, but hopefully it will be useful for anyone wanting to Puppetize their NFS servers - which of course you should be.

