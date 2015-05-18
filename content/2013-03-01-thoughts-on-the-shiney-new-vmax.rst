Thoughts on the shiney new VMAX
###############################
:tags:  storage

{% img right
https://www.emc.com/R1/images/EMC\_Image\_C\_1310593327367\_header-image-vmax-10k.png
%} I've spent a significant amount of time recently swatting up on EMC's
new `VMAX Cloud
Edition <https://chucksblog.emc.com/chucks_blog/2013/02/introducing-vmax-cloud-edition.html>`__.
It has to be said that this looks like one of the most interesting
storage announcements I have seen in a long time. In fact I have a
project coming up that I think it may well be a perfect fit for.

First a massive thanks to EMC's Matthew Yeager (@mpyeager) who answered
a couple of questions I had. He really went the extra mile to clarify a
couple of things and the
`video <https://www.youtube.com/watch?v=WoElTAevLDs>`__ he made is well
worth a watch. Also Martin Glassborow (@storagebod) has `interesting
things to say <https://www.storagebod.com/wordpress/?p=1293>`__ as well.

This is a product that could put a lot of people out of a job. If you
are the sort of person who likes to keep hold of your little castle's of
knowledge then you will not like this from what I can see. Finally we
are able to be truly customer focused, balancing cost, performance and
capacity to give them exactly what they want. EMC claim this is a world
first and to my knowledge they are right.

{% pullquote %} Storage architects put a lot of time and effort in to
tweaking quotes and systems to balance price, capacity and performance
for a given work load. However, most of this is just reading up on the
best-practises for a given array and situation and applying them. There
is nothing that clever to it - reading and practise is what it comes
down to. However, it has alway been as much an art as a science because
an individual architect does not have a very large dataset to refer to.
On the other hand EMC have got 60 million hours of metrics across more
than 7000 VMAX systems out in the field. {" With that amount of data the
amount of art involved diminishes "} and it becomes purely a science. {%
endpullquote %}

What you get is a `VMAX
10k <https://www.emc.com/storage/symmetrix-vmax/vmax-10k.htm>`__, but
instead of defining storage pools, tiering policies, RAID levels etc you
balance 3 facters: Space, performance and cost. Need a certain
performance level for a certain amount of space no matter the cost? Just
dial it in and mail EMC a cheque. Have a certain budget, need a certain
amount of space, but performance not a problem? Same again.

No longer will we be carefully balancing the number of SATA and FC
spindles and the types of RAID level. No longer will be worrying about
what percentage of our workload we need to keep on the SSD layer to
assure the necessary number of IOPS. We will not even be calculating how
much space we have after the RAID overheads.

{% pullquote %} That is all very interesting, but so far it is just a
new approach to the UI. It is an excellent approach, but nothing
especially clever. One of things I gravitated towards was the white
paper about integrating with
`vCloud <https://www.emc.com/collateral/white-papers/h11468-vmax-cloud-edition-wp.pdf>`__.
Despite it being geared toward VMware (I wonder why? - not!) the
principles equally apply to any situation where automation is required.
I am a huge DevOps fan (Puppet in particular). Storage arrays have never
been particularly automation friendly. In addition to the cloud portal,
the VMAX CE also has a RESTful API. Now that is awesome! {" Here we have
the abilty to easily integrate a VMAX with the likes of OpenStack
Cinder, Puppet, Libvirt, or whatever "} you want. {% endpullquote %}

Finally `Chad Sakac <https://virtualgeek.typepad.com>`__ informs me that
VMAX CE is just the first. EMC intend to roll this management style out
to other product lines. Personally I think this would suit both Isilion
and Atmos lines very nicely.

I am really excited about this product. It brings a paradigm shift in
storage management and automation. Also I am led to believe that the
price is exceptional as well, to point that it seems EMC may even be
pushing VNX down a market level (to where it should be perhaps?). I have
been `a bit
nasty <{{%20root_url%20}}/blog/2012/12/10/emc-extremio-thoughts/>`__ to
EMC in the past, but recently they are doing some stuff that has really
got me interested. This and
`Razor <https://github.com/puppetlabs/Razor>`__ are 2 projects that are
definitely worth keeping an eye on.

.. raw:: html

   <iframe width="420" height="315" src="https://www.youtube.com/embed/WoElTAevLDs" frameborder="0" allowfullscreen></iframe>


