title: "Music Player Daemon in Fedora"
date: 2012-03-16 22:04
comments: true


This should have nice and simple, but there was a little gotcha (for me anyway).

First install the RPMFusion repositories:
<!-- more -->
```
yum localinstall --nogpgcheck \
    https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm \
    https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm
```

Now you can install MPD and a simple client with
```
yum install mpd mpc
```

By default it looks in _/var/lib/mpd/music_ which strikes me as reasonable, so copy some music there. Now comes the bit that caught me out; you will need to update is library:
```
mpc update
```
A lot of documentation on the net talks about running `mpd –create-db`, but this is now depreciated. I eventually found this out on Arch Linux’s wiki.

Connect a client and listen to your music – I’m using gmpc (`yum install gmpc`) which is very feature rich, but if you want something simpler, try Sonata (`yum install sonata`) or even _mpc_ itself. Finally you can also use you MPDroid on your phone.

