How I Classify Puppet Nodes
###########################

:slug: how-i-classify-puppet-nodes
:date: 2015-08-18
:tags: devops
:summary: 
:status: draft

The basics of defining what modules get applied to a particular node is really simple in Puppet. Out of the box you just use the hostname and the FQDN and everyone is happy. You find this everywhere in documentation, blog posts, presentations, etc. However is has a problem: scale.

What if you have an elastic infrastructure with nodes being created and destroyed automatically? What if you want to use the same manifests in different environment, but use different hostnames? What if you have stupidly complex host naming conventions that you cannot get your head round (current day job problem for me :-( )?

In all these cases and more, using the hostname to classify the node falls down. I like to add in `Role` that can then be access in 2 ways. With Hiera, one could do something like:

.. code:: yaml

    :hierarchy:
      - "nodes/%{::trusted.certname}"
      - "roles/%{role}"
      - "%{environment}"
      - "%{osfamily}-osreleasemajor"
      - global

And with in ``site.pp`` we can add in a simple ``case`` statement:

.. code:: puppet

    node default {
      case $::role {
        'loadbalancer': {
          class { 'haproxy': }
        }
        'db': {
          class { 'mysql': }
        }
        default: {
          notify('no specific classes assigned')
        }
      }
      class { 'security': }
    }

Now, we can still classify nodes individually but there is something in between the wider environment and OS categories that we can define ourselves. Of course we now need to define the role, which is everywhere from simple to complex or even not completely clear in my head for now.

I create a custom `role` fact that my manifests will look at. This is universal, no matter what mechanism is used to populate that fact that is the only place I will search in my Puppet code.

When your nodes are under Openstack or EC2, this is simple. They both have the concept of user-defined metadata as key-value pairs. I simple add a `role` pair:

.. code:: shell

    nova meta <instance-id> set role=loadbalancer

You can also set this when you create the instance.

.. code:: shell

    nova boot --meta role=loadbalancer --<other-settings> <hostname>

Now we just need the fact to look it up.

.. code:: ruby

    require 'net/http'
    require 'json'
    require 'uri'

    module RoleModule
      def self.add_facts
        Facter.add("role") do
          productname = Facter.value(:productname)
          case productname
          when 'OpenStack Nova'
            setcode do
              url= "http://169.254.169.254/openstack/latest/meta_data.json"
              uri = URI.parse(url)
              http = Net::HTTP.new(uri.host,uri.port)
              response = http.get(uri.path)
              JSON.parse(response.body)['meta']['role']
            end
          when 'ProLiant MicroServer'
            setcode do
              'lab-compute'
            end
          end
        end
      end
    end
    RoleModule.add_facts

What is happening here? First it checks the `productname` fact so it can work out what to do. If that is `OpenStack Nova` then it knows that is needs to look in the Openstack Metadata service (http://169.254.169.254/openstack/latest/meta_data.json). Our key/value pair is returned as part of that JSON data and is pushed in to the `role` fact.

Likewise, if the `productname` is an HP Microserver, it will always be a lab compute node (in my case).

Physical machines otherwise fall down here. There is no way to dynamically modify their role, but I have a couple of solutions:

- Part of the kickstart file for provisioning the node could populate a configuration file (``/etc/role.conf``). If the ``virtual`` fact contains ``physical`` the role fact goes and looks it up from there.
- A seperate node classification service that returns a role based on the contents of various facts that are passed via the custom fact code.

The important part with both of these is the classification is totally seperate from my Puppet code.
