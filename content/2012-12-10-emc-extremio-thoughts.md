---
layout: post
title: "EMC ExtremIO Thoughts"
date: 2012-12-10 16:39
comments: true
categories:  storage
---
There has been quite a bit of musing recently on the web about EMC and what will come out of their ExtremIO acquisition. They have recently (finally) started demonstrating an all-flash array. The name says it all: ExtremIO. It is for super high IOPS applications - Virtual desktops, enormous DBs, that sort of thing.
<!-- more -->

It is a bit of a depature from traditional EMC, in that it [appears](http://storagenewsletter.com/news/systems/all-ssd-system-from-emc-xtremio-) that it is going to be a true scale-out architecture. This is has more in common with Isilion (not developed at EMC) than VMAX (developed at EMC).

The problem is that EMC are *extremely* late to the market this time around. VMAX was ahead of the curve by adding flash. In the all flash arena there are several options already there, [Violin](http://violin-memory.com), [Whiptail](http://whiptail.com/) spring straight to mind.

Over at [The Storage Architect](http://blog.thestoragearchitect.com/2012/12/10/xtremio-aka-project-x-wheres-the-innovation/) Chris Evans gives the standard counter-arguments to EMC's marketing spin. Namely:

1. Other vendor solutions aren't as resilient
2. It's a 1.0 product, expect more from 2.0 and beyond
3. It gives our customers choice

I hate to say it, but EMC have one HUGE advantage over all the startups. Quite simply they are EMC! As experts we know that Violin (for example) have a more mature product than EMC do.

{% pullquote %}
{"When the guy with the credit card sees the name "EMC" it will be hard to persuade him that such a mature brand has the more immature product"}. This won't be the case everywhere, but in a lot of large enterprise they would go to their storage experts (like me) and ask for advice on which flash array to go for; they then stipulate that it has to come from EMC's portfolio. At which point I through my hands up in despair, tell the to buy ExtremIO, the guy who has the better, more mature, solution loses the business that was rightfully theirs.
{% endpullquote %}

It is not a 1.0 product, I can not accept that EMC acquired ExtremIO based on stuff that was only on paper. At best this is a 1.5 product, but realistically it is a 2.0 product. From a company with the resources of EMC, this should be coming out of the blocks running - it should be the best in class. OK, ExtremIO were further from version 1.0 than EMC were maybe lead to believe at the time, but they have got a lot of resources. After a year, they should not be in damage control mode.

Does it really give the customers choice? I would go one step further than what Chris has said - that an all-flash VMAX or VNX would have made sense. I agree with him, but I also think that they have actually removed choice.

I would say that EMC have cocked-up here. They under-estimated the market for all-flash arrays. Even my [old employer have got some](http://www.violin-memory.com/news/press-releases/nats-selects-violin-memory-flash-storage-for-virtual-desktop-infrastructure/) and that is in Air Traffic control - there is no-one else who relies more on "tried and tested" technology than them. They then rushed to through some money at the problem, but like of Violin were already happy where they were.

{% pullquote %}
Robin Harris at [StorageMojo](http://storagemojo.com/2012/12/05/emcs-xtreme-embarrassment/) thinks this will be a costly mistake for EMC. I disagree, I think by announcing that this is coming EMC will stall the market and thus come out of this fine. Unfortunately there is too much latency in the enterprise storage space for it to be otherwise. I wish it were a bit more dynamic and {"I wish that EMC would be punished for this"}, thus rewarding one of the underdogs. That does not happen enough in the enterprise space, especially for an Englishman like me (we do love the underdogs).
{% endpullquote %}
