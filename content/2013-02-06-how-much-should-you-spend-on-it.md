title: "How much should you spend on IT"
date: 2013-02-06 16:04
comments: true

A recent discussion/argument I had on Reddit got me thinking about the cost of solutions we put in.

In an ideal world everything would did have full redundancy, and the customer would never have any downtime. Everything would always be up-to-date and keeping it so would require restarting. The reality is very different unfortunately.
<!--more-->

This potentially rambling post was inspired by someone accusing me of having "a horrible idea" because I suggested someone put pfsense on an Atom PC as a VPN router for a small office. He then proceeded to expain to me how you should always buy an expensive black box from a vendor (he didn't say black box if I am honest, I am interpreting), how you have to always have support on absolutely everything. I called 'bullshit' and the whole thing went round in circles a bit until we both realised that were actually singing from the same song sheet, but from different ends of the room.

{% pullquote %}
When looking at a solution {" it is always necessary to look at the actual requirements of the end-user "}. I had a conversation with a Director at $lastjob once. We had recently had a planned outage on the website for a few minutes one Sunday night so I could de-commission the old SAN. He said that he wanted us to get to 99.999% IT uptime. My reply after some quick calculations was that we had actually achieved that for the last 3 years at least, but that I would not like to guarantee it in the future with our current and planned infrastructure. This lead to him asking me to go ahead and do the calculations on how to guarantee it. When I went back to him with my figure (done using lots of Open Source, and no vendor support) he changed his mind. This was in what would be classed as an SME - heading towards £100 million a year turnover and one of world's best in their field. Not a small company by any means, but they could not justify that cost.
{% endpullquote %}

Having said that they could justify a lot. All our servers were clustered, storage was Fibre-channel, they had a 100TB 8Gb array for a team of 2 people who crunched monster video files all day. All that was justified expenditure, but they were not an internet company, so a bit of downtime could be justified. Even when we had a major disaster and a large swathe of Linux VMs disappeared from this world, nobody actually had to stop working and no money was lost.

A small business is not going to dump the money for multi-thousand pound Cisco router and a zero-contention synchronous internet connection. They may think that they need the best of everything, they may even be willing to pay for it if they have got enough of daddy's funding behind them. However that would be foolish, that money would be better spent on giving everyone a Christmas bonus.

Support contracts are another bone of contention. Now everything I have is under one, but that is not always necessary. I once needed to get a couple of TBs of storage into a large office asap. I happenned to have a few FC HBAs, a couple of old Proliants and a pile of MSA1000s in a cupboard. I built up a box with a pair of HBAs and a single MSA1000 and sent the whole lot up to the office with strict instructions that all the extras were for spares only. If something broke, no need for support - just swap it out. I figured it would be good for at least another 3 years. Especially as backups were pretty reliable there. Would a new SAN with expensive support have been more reliable, I doubt it. We would have to wait 4 hours for a new disk, rather than the 5 minutes a took to walk to the cupboard.

{% pullquote %}
It is not always necessary to get the shiniest stuff, with the longest/quickest support contract. We know our gear, we know how reliable it is, we know how long it lasts. The people paying the bills do not, they rely on us to advise them honestly and wisely. That {" wisdom can fall at either end of the price-spectrum "}, but needs to be based on the ACTUAL risks and their effect. 
{% endpullquote %}
