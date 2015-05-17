title: "Install Microsoft TrueType fonts on Fedora"
date: 2014-07-28 11:01
comments: true
{% img right https://i.imgur.com/IVNu1pf.png %} Fedora do nogt bundle Microsoft's core Truetype fonts for licensing reasons. Normallly I do not care, personally I prefer [Liberation fonts](https://fedorahosted.org/liberation-fonts/) anyway. However, today I needed to Verdana.
<!-- more -->

Traditionally, the way to install these on RPM based distributions has been:

1. Grab the RPM spec file
2. Build an RPM from the spec file
3. Install RPM using the `rpm` command.

All well and good, however there are a couple of problems.

- Using RPM directly is frowned upon

Nowadays, Yum does various bits of house keeping in addition to RPM, so this can lead to the `rpm` and `yum` databases getting their knickers in a twist.

I get around this with a simple piece of `sed`/`grep`:

```
curl https://corefonts.sourceforge.net/msttcorefonts-2.0-1.spec | grep -v 'Prereq: /usr/sbin/chkfontpath' > msttcorefonts-2.0-1.spec
```

Now you can do all the usual stuff:

```
rpmbuild -ba msttcorefonts-2.0-1.spec
yum --nogpgcheck ~/rpmbuild/RPMS/noarch/msttcorefonts-2.0-1.noarch.rpm
```

Relogin and you will have access to Microsoft's fonts.
