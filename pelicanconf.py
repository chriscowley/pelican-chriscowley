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
PLUGINS = [ "gravatar" ]

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
