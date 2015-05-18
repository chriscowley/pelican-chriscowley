What will HP do next?
#####################
:tags:  storage

HP recently announced a new range of 3Par based arrays that are aimed at
mid-range enterprise. There now appear to be 2 ranges for the future:

-  HP StoreServ 10000 is the big boy, scales up to 1.6PB, 192 FC ports,
   32 10Gb iSCSI - the works.
-  HP StoreServ 7000 is the mid-range one, with *only* 24 FC and 8 1-Gb
   iSCSI. This split into the 7200 (2U) and 7400 (4U)

With the entry level `7200 starting at
$20k <https://www8.hp.com/us/en/hp-news/press-release.html?id=1332554#.UM8Mm3eTW01>`__
that does not leave a lot of room at the low end for both the P4000 and
the P2000 ranges. At the higher end the 7400 starts at $32k, which
certainly leaves no space for the venerable EVA.

In `an interview with Around the Storage
Block <https://h30507.www3.hp.com/t5/Around-the-Storage-Block-Blog/Blogger-Q-amp-A-with-David-Scott/ba-p/128097>`__
HP Storage GM David Scott is quite critical of EMC who have a range of
different and fairly unrelated product lines (Atmos, VMAX, VNX/VNXe,
Isilion). For now HP is fairly similar: P9000 (Hitachi), P4000
(Lefthand, P2000 (Dot Hill). When you look at where they have priced the
3Par gear, it does appear that they are betting the farm on it.

Something I have been quite vocal about over the last 5 years or so is
that fact that HP's storage portfolio is all over the place. Compared to
Netapp, who have a very homogenous portfolio (everything runs OnTAP, you
know one Netapp product, you can jump on to the rest), HP have got a one
interface for P2000, another for P4000, another for EVA. Nothing sits
together. HP needs to get all this in line. EMC have already started
with Unisphere, but they still have multiple product architectures
(VMAX, VNX, Isilion for example).

I personally think that these other ranges will drop by the wayside,
although I am reading a bit between the lines here. Dot Hill do seem to
be setting themselves up to be more than just an OEM supplier to HP.
Maybe it is wishful thinking as I am a `huge fan of Dot
Hill <https://www.chriscowley.me.uk/blog/2010/01/12/some-great-new-san-gear/>`__,
but they have some very interesting products. I hope/expect to see a lot
more of Dot Hill themselves over the next few years, rather than just
being behind Oracle/Netapp/HP badges.

The P9000 range is a similar story at the other end of the market. The
Storserve 10k seems to be very similar, pretty much the same capacity
and number of ports. Feature set is also close enough. I also have the
impression that Hitachi are starting to push a bit harder in their own
right as well.

Essentially I think 3Par will become HP's own architecture. It has the
flexibity to cover everything from a single bay with 12 SATA disks at
the low end (perhaps on DL hardware) all the way up to PB+ scales,
taking in all-flash on the way.

This leaves the P4000, which has been re-branded the `StoreVirtual
4000 <https://www8.hp.com/us/en/products/disk-storage/product-detail.html?oid=4118659>`__.
This seems to me to be a no-brainer. It is already running on commodity
DL180 hardware and includes an appliance option. My guess is the
physical implementation of this will be phased out. It will become the
Virtual Appliance front-end to all this new 3Par based physical
goodness.

Finally, I have skipped over the EVA. What does the future hold in store
for HP's venerable high-end platform. I think nothing. It will go into
maintenance mode and be quietly end-of-life'd. Existing customers will
be pushed to
`migrate <https://h30507.www3.hp.com/t5/Around-the-Storage-Block-Blog/EVA-to-HP-3PAR-StoreServ-online-import/ba-p/128391>`__
over to Storeserv 7000.
