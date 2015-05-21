Logstash on CentOS 6
####################
:tags:  monitoring

.. figure:: http://logstash.net/images/logstash.png
    :align: right
    :width: 200
    :alt: log

It's been a while since I last posted anything, but it is time to. 
I've been playing around a lot with various tools for gathering
information about my environment recently. One of the most important tools
for storing that information is decent logging. Syslog is proven and solid,
but a little creaky. For storing everything it is fine, but getting anything
out is not so great.

Logstash is an awesome tool written by `Jordan
Sissel <https://twitter.com/jordansissel>`__ that is used to "collect
logs, parse them, and store them for later use (like, for searching)".
It has an excellent howto, but I have one problem with it: the use of a
tar file rather than packages. This easily worked around though, as
Elasticsearch have it in their Yum repository.

First up, define that repository in the file
``/etc/yum.repos.d/logstash.repo``:

::

    [logstash-1.4]
    name=logstash repository for 1.4.x packages
    baseurl=https://packages.elasticsearch.org/logstash/1.4/centos
    gpgcheck=1
    gpgkey=https://packages.elasticsearch.org/GPG-KEY-elasticsearch
    enabled=1

    [elasticsearch-1.0]
    name=Elasticsearch repository for 1.0.x packages
    baseurl=https://packages.elasticsearch.org/elasticsearch/1.0/centos
    gpgcheck=1
    gpgkey=https://packages.elasticsearch.org/GPG-KEY-elasticsearch
    enabled=1

The rpm does not create its user and group, nor does it create the PID
directory for Kibana. Create those then install Łogstash:

::

    mkdir /var/run/logstash-web
    yum -y install logstash elasticsearch logstash-contrib.noarch mcollective-logstash-audit.noarch
    chkconfig --add elasticsearch
    chkconfig elasticsearch on
    service elasticsearch start

For the installation that is it. When you reboot the services will start
and you are good to go. Before rebooting though it is worth playing
around a little. So lets blatantly rip off the
`Quickstart <https://logstash.net/docs/1.4.0/tutorials/getting-started-with-logstash>`__.
Run:

::

    sudo -u logstash /opt/logstash/bin/logstash -e 'input { stdin { } } output { stdout { codec => rubydebug } }'

Logstash takes a while to get going as it needs to fire up the JRE
(hint: run ``htop`` in another terminal to see when the Java process
calms down). When it is happy type (in the same console you started it
in) ``hello``. You should see something like:

::

    hello
    {
           "message" => "hello",
          "@version" => "1",
        "@timestamp" => "2014-03-21T20:56:58.439Z",
              "host" => "monitor.chriscowley.lan"
    }

That is not very interesting unfortunately. It just takes STDIN, the
logs it to STDOUT in a funky format. This all gets more interesting when
you start storing your logs somewhere. A good choice is (funnily enough)
Elasticsearch. This time run Logstash with this as the output:

::

    sudo -u logstash /opt/logstash/bin/logstash -e 'input { stdin { } } output { elasticsearch { host => localhost } }'

Now if you type something in that same console (we're still taking the
input from STDIN) the output will be written to Elasticsearch.

To test that run ``curl 'https://localhost:9200/_search?pretty'`` in
another console and you should see something like:

::

    {
      "took" : 11,
      "timed_out" : false,
      "_shards" : {
        "total" : 5,
        "successful" : 5,
        "failed" : 0
      },
      "hits" : {
          "_index" : "logstash-2014.03.21",
          "_type" : "logs",
          "_id" : "aRFzhx-4Ta-jy_PC50U7Lg",
          "_score" : 1.0, "_source" : {"message":"you know, for logs","@version":"1","@timestamp":"2014-03-21T21:01:17.766Z","host":"monitor.chriscowley.lan"}
        }, {
          "_index" : "logstash-2014.03.21",
          "_type" : "logs",
          "_id" : "VP8WcqOYRuCbpYgGA5S1oA",
          "_score" : 1.0, "_source" : {"message":"another one for the logs","@version":"1","@timestamp":"2014-03-21T21:03:42.480Z","host":"monitor.chriscowley.lan"}
        } ]
      }
    }

Now that does not persist when you kill Logstash. To do that create a
file in ``/etc/logstash/conf.d/`` that contains this:

::

    input {
      file {
        path           => "/var/log/messages"
        start_position => beginning
      }
    }

    filter {
      if [type] == "syslog" {
        grok {
          match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
          add_field => [ "received_at", "%{@timestamp}" ]
          add_field => [ "received_from", "%{host}" ]
        }
        syslog_pri { }
        date {
          match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
        }
      }
    }


    output {
      elasticsearch {
        host => localhost
      }
      stdout { codec => rubydebug }
    }

That gives you a simple setup for storing everything in that systems'
syslog. The logical next step from there is to enable that host a
central syslogger. This well documented elsewhere, but simplistically
you need to add the following to ``/etc/rsyslog.conf``:

::

    # Provides UDP syslog reception
    $ModLoad imudp
    $UDPServerRun 514

    # Provides TCP syslog reception
    $ModLoad imtcp
    $InputTCPServerRun 514

There is a single final step due to the fact that /var/log/messages is
only readable by *root*. Normally this is a big faux pas, but I am
putting my trust in Jordan Sissel not to have sold his soul to the NSA.
To read this (and connect to ports below 1024) Logstash needs to run as
*root*. Edit ``/etc/sysconfig/logstash`` and change the line:

::

    LS_USER=logstash

to read:

::

    LS_USER=root

Now you can start Logstash and it will pull in ``/var/log/messages``:

::

    service logstash start

There are loads of configuration options for Logstash, so have a look in
the `main documentation <https://logstash.net/docs/1.4.0/>`__ and the
`Cookbook <https://cookbook.logstash.net/>`__ for more.
