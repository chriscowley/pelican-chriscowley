#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Cowley'
SITENAME = u'Just Another Linux Blog'
SITEURL = ''
AUTHOR_EMAIL = "chris@chriscowley.me.uk"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
THEME = "/home/chris/Development/pelican-themes/pelican-bootstrap3"
BOOTSTRAP_THEME = "cosmo"
PLUGIN_PATH = "/home/chris/Development/pelican-plugins"
PLUGINS = [ 'gravatar', 'liquid_tags.img', 'liquid_tags.video',
            'liquid_tags.youtube', 'liquid_tags.vimeo',
            'liquid_tags.include_code' ]

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/')
#         )

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/chriscowleyunix'),
          ('github', 'http://github.com/chriscowley'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = [ 'images', 'assets' ]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

DISQUS_SITENAME = "justanotherlinuxblog"
GOOGLE_ANALYTICS = "UA-32843690-1"
