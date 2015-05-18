DevOps Terminology
##################
:tags: devops

Talking to a few people there seems to be a little confusion over the
various stages in the deployment pipeline. Specifically there seems to
be a little confusion over 3 things:

.. raw:: html

   <!-- more -->

-  Orchestration
-  Provisioning
-  Configuration Management

These seem to have got rather mixed up of late. I will put the blame
squarely at the doors of marketing departments because, well, why not...

I should probably add that these are my opinions. It is all a little
grey, but this makes sense to me.

To me Configuration Management should be every single environment, no
matter how simple. By contrast the other 2 may not apply everywhere. Its
basic role is to take your basic system and prepare it for production.

It is also an ongoing process, because it does not only apply your
configuration. Once everything is going it continues to enforce that
configuration.

A benefit that comes from this is that it should also be effectively
self-documenting.

Personally I always head towards `Puppet <https://www.puppetlabs.com>`__
here. There are plenty of good options though, such as Ansible and
Saltstack.

Working back, provisioning should deploy the most basic system that can
hook up to your configuration management system.

    Personally I do not like templates, à la VMware. Rather I prefer to
    just to do fresh OS install. That way I do not need to perform a
    second pass to install updates. Having said that, when working with
    AWS or Openstack they are a very effective way to work

The key thing here is that it should link in with the next step
(configuration management). It is essentially that it hands the new
system over to CM with no input from the SysAdmin. As a Puppet user this
means that you should come out at the end with the Puppet agent
installed and configured.

I tend towards `Razor <https://github.com/puppetlabs/razor-server>`__
which is truly excellent. There are other good options such as
`Cobbler <https://www.cobblerd.org/>`__, but basically anything that can
perform an OS install, add an agent and inject a config file is great.
In many environments, a simple PXE server with a bunch of kickstart
files may well be more than sufficient.

Orchestration is the first stage that provides an automated way of
launching your provisioning system. It also prepares the Configuration
Management. In my ver Puppet-centric world this means it should
configure Hiera data for what the new system(s) are to do.

It terms of tooling, there is always a certain amount of
cross-pollination. Puppet for example can be used as an excellent way of
`controlling your AWS
infrastucture <https://puppetlabs.com/blog/provision-aws-infrastructure-using-puppet>`__
which puts it firmly in the provisioning camp. I will not tell anyone
not to use it that way, but I personally see it as a little
*feature-creep*-like, so I will not be going there. I will be sticking
to the tried and tested UNIX philosophy of "do one thing and do it
well".
