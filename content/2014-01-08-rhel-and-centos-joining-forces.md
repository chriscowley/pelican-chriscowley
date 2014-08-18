title: RHEL and CentOS joining forces
comments: true
categories: linux

![RHEL and CentOS logos](http://i.imgur.com/3colCNj.png){: style="float:right"}Yesterday saw probably the biggest FLOSS news in recent times. Certainly the biggest news of 2014 so far :-) By some freak of overloaded RSS readers, I missed the announcement, but I did see this:

<blockquote class="twitter-tweet" lang="en"><p>Day 1 at the new job. Important stuff first.. Where do I get my Red Hat ?</p>&mdash; Karanbir Singh (@CentOS) <a href="https://twitter.com/CentOS/statuses/420876286785892353">January 8, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
<!-- more -->

It did not take long to dig up [this](http://community.redhat.com/centos-faq/?utm_content=buffer6403d&utm_source=buffer&utm_medium=twitter&utm_campaign=Buffer) and [this](http://lists.centos.org/pipermail/centos-announce/2014-January/020100.html), where Red Hat and CentOS respectively announce that they have joined forces. Some things from the announcement struck me:

>  Some of us now work for Red Hat, but not RHEL

That is important! This says to me that Red Hat see the value of CentOS as an entity in itself. By not linking the CentOS developers to RHEL in anyway, they are not going to be side-tracking them. Instead, they are simple freeing them up to work more effectively on CentOS.

> we are now able to work with the Red Hat legal teams

QA was always a problem for CentOS, simply because it took place effectively in secret. Now they can just walk down the corridor to talk to the lawyers who would have previously (potentially) sued them, all the potential problems go away.

# The RHEL Ecosystem

{% pullquote %}
In the beginning there is [Fedora](http://fedoraproject.org)), where the RHEL developers get to play. Here is where they can try new things and make mistakes. {"In Fedora things can break without people really worrying"} (especially in Rawhide). The exception to this is my wife as we run it on the family PC and she gets quite frustrated with its foibles. However, she knew she was marrying a geek from the outset, so I will not accept any blame for this.
{% endpullquote %}}

Periodically, the the Fedora developers will pull everything together and create a release that has the potential to be transformed into RHEL. Here they pull together all the things that have be learnt over the last few releases. I consider this an Alpha release of RHEL. At this point, behind the scenes, the RHEL developers will take those packages and start work on the next release of RHEL.

{% pullquote %}
On release of RHEL, Red Hat make the source code available, as required by the terms of the GPL (and other relevant licenses).The thing is, {"Red Hat as a company are built on Open Source"} principles, they firmly believe in them and, best of all, they practise what the preach. They would still be within the letter of the law if the just dumped a bunch of apparently random scripts on a web server. Instead, they publish the SRPM packages used to build RHEL.
{% endpullquote %}

CentOS then take these sources and get to work. By definition they are always beind RHEL. As many know this got pretty bad at one point:

{% img http://www.standalone-sysadmin.com/~matt/centos-delays.jpg center %}

(Thanks to Matt Simmons, aka [Standalone Sysadmin](http://www.standalone-sysadmin.com), from whom I blatantly stole that graph, I'll ask permission later)

Since then, things have got better, with new point releases coming hot on the heels of RHEL. Certainly preparations for EL7 seemed to be going on nicely even before this announcement.

# how does this now affect the two projects
Both CentOS and Red Hat have a lot to gain from this alliance. {% img right http://i.imgur.com/qbKvXko.jpg 350 350 %}I am sure that there are few people in the wider community who will be upset, but I think that it is a good thing. The reality is that CentOS and RHEL have never been enemies. The people that are using CentOS are just simply never going to pay Red Hat for support they do not need.

When I started at Snell (then Snell & Wilcox), the official line was to use RHEL for all our Linux servers. They had everything paid up for a couple of years at the time. By the time renewal came around the global financial crisis had hit, we had used the support two or three times and each time I had solved the problem before Red Hat answered the ticket. So, we decided to switch to CentOS (which was trivial).

At the other end of the scale you have the web-scale people. For them, paying Red Hat for support is both unnecessary (they have the right people on staff) and prohibitively expensive. When you have tens of thousands of nodes you cannot use a licensing model that support each one.

In the cloud model you also have a problem, in that you are effectively renting an OS. Microsoft and Red Hat you have an administrative overhead of ensuring you have the right licenses available. In my experience Red Hat make it a lot easier, but it is an overhead none the less.

All three of these will get a huge benefit. Now that the CentOS developers are on staff at Red Hat they have direct access to the source code. There should no longer be any need to wait for RHEL to drop before they start building. Red Hat will be supplying infrastructure and community support, which will also be a massive bonus.

So what do Red Hat gain? In terms of new customers, they may get some of that first group. These are the people that may well do their testing with CentOS, but may now choose to go production with RHEL. I certainly would be more willing to now that XFS is not in a separate (expensive) RAN channel. I do not see the cloud or web-scale people changing to a paid support model. It will remain prohibitively expensive for them.

I think they biggest thing that Red Hat will gain is that get to give Oracle a good kicking. Oracle basically do the same thing as CentOS, but they stick a thumping great big support charge on it. To be honest I have never really worked out why anyone would use it. Yes they are cheaper than Red Hat, but not by much. A couple of years ago Red Hat took steps to [make life harder](http://www.theregister.co.uk/2011/03/04/red_hat_twarts_oracle_and_novell_with_change_to_source_code_packaging/). That had an unfortunate knock-on effect on CentOS, causing the huge delay in CentOS 6. Now CentOS should not have that problem as they are closer to source.

# TL;DR
CentOS and RHEL joining forces is in my opinion a really good thing, with both parties getting significant benefits. Granted they are bit less tangible for Red Hat, but that does not make them any less significant.

Personally I am really excited to see what it is in store - especially from CentOS. I even have a couple of SIG ideas too.
