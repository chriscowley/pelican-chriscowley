title: "Bootstrapping a Puppet master"
Date: 2015-03-14 21:21
comments: true
Installing a Puppetmaster is a bit of a chicken-egg problem. We want to have our environment as automated and slick as possible, but we currently have no tools installed to to so.

<!-- more  -->

So what do we actually need to install and configure for our Puppet master:

   - Puppet
   - Hiera
   - R10k
   - Git

This is the minimum, from this it can go ahead and dogfood itself in my prefered fashion.

I do this with a bit of bash that I threw together during a meeting. I use only bash as that is the only thing I can be guaranteed to have on a clean install.

If you trust me then simply run:

```
curl https://raw.githubusercontent.com/chriscowley/puppetmaster-bootstrap/master/bootstrap.sh | sudo -E sh
```

If not, or of you want to control it a bit more, then clone it. If you modify it I'll happily accept pull requests.

```
git clone https://github.com/chriscowley/puppetmaster-bootstrap.git
cd puppetmaster-bootstrap
./bootstrap.sh
```

There are a few environment variables you can use to control it:

   - PMB_CONFIGURE_GIT : Whether to install/configure Git (defaults=1)
   - PMB_CONFIGURE_R10k : Whether to install/configure R10k (defaults=1)
   - PMB_TEST : Only tell you what it would do, but nothing actually happens
   - PMB_INSTALL_POSTRECEIVE : Install the post-receive git hook (default=1)

I have tried to use sensible defaults, at least for my purposes.
