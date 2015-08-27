All Backup Solutions Suck
#########################
:slug: all-backup-solutions-suck
:date: 2015-08-27
:tags: opinions

Recently I have been working a lot on a backup solution at work, which
has been a painful experience to say the least. Why? Simply because
there is no solution that meets my ideal requirements. These are pretty
precise:

-  Open Source
-  Openstack Swift as a backend
-  File level restores
-  Scalable
-  Lightweight
-  An idiot must be able to restore a file
-  Not a source of truth about my infrastructure
-  Automated restore testing

A nice bonus would be volume level backups of Openstack Cinder.

From what I can tell, nothing currently out there meets these
requirements. If I take away the Open Source requirement it does not get
much better. `Rubrik <http://www.rubrik.com>`__ looks interesting, if it weren't tied into VMware, as are a few other solutions.

Nothing meets my needs :-( Naturally this has got me thinking about how
something like this could be achieved, so here goes.

I am actually taking my inspiration from the monitoring world, where
there has been similar problems. In the past, one just went straight for
Nagios to do alerting and Munin/Cacti for storing metrics. For various
reasons these just sucked, but the big one for me was this:

    I had to tell it what it had to monitor!

Tomorrow, I may be called upon to deploy a Hadoop cluster with 100
slaves. All of these would have to be individually added to Nagios. This
invariable got forgotten and before long nothing was monitored and
Nagios was forgotten about. Things broke, nobody knew about it. Everyone
said "IT SUCKS".

However, recently I've been playing around with
`Sensu <http://www.sensuapp.org>`__. This works the other way round. The
node announces itself to the server, which has a set of rules that that
the node uses to monitor itself. This, allied with all the comms being
over a Message Queue, makes it astoundingly scalable.

This is the sort of principle that backup should follow.

You have a central server, which is essentially just an API that a node
can query to discover what to do. This is based on rules such as cloud
metadata, hostname, subnet, whatever else takes your fancy. As this
server is just an API, we can use an HTTP load balancer and a NoSQL
database to improve availability and scaling.

A new agent comes online, after being installed by my CM system. It
queries the API to find out what to do, it the takes it from there. The
only time it will interact with the central server is when its
configuration changes. It knows what to backup and where to put it, so
off it goes. It can use existing tools: ``tar``, ``bzip2``,
``duplicity``, ``gpg`` etc and push it directly into the storage desired
(S3/Glacier or Openstack Swift would be the best choices I'd say).

Of course I mindful that not all nodes will have direct access to the
storage backend for many reasons. In this case, it could use the Load
Balancer already used for the server API to bounce off to the storage.
After all, this is just an HTTP stream we are talking about; even a
fairly lightweight HAProxy instance will be able to handle 100s of
streams.

So on paper, what this should give us is a backup solution that is:

-  Scalable: as there is no need to define nodes on a central server,
   there is no extra step when configuring an new node. You deploy it,
   install the agent and it just works. Perhaps one could follow the
   Puppet model, where it defaults to a certain hostname as the server.
   If that is in your DNS, then you do not even need to configure the
   agent.
-  High performance: The processing is distributed accross literally
   your entire infrastructure, so your backup server does not become a
   bottleneck.
-  Has no single point of failure: If your server is just a REST API and
   a web app, then HA can be performed easily with well understood
   techniques. Even if you do lose it, your backups do not stop as the
   nodes are doing it all themselves.
-  Restores use standard tools: If you have lost everything, there is no
   need to bring up your backup infrastructure first in order access
   your data. It is stored on a standard backend, created with standard
   tools that are available on any node with just a simple
   ``apt-get``/``yum``.

All this seems obvious to me, so why has no-one done it?

Of course, a genuine backup product needs do do reporting and things like that. This is another role the central server could take on: it has a MongoDB cluster to store all that in. Or, that could be an "add-on" that just hooks into the same MongoDB (UNIX principal: do one job, and do it well).
