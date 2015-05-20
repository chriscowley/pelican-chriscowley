#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Cowley'
SITENAME = u'Yet Another Linux Blog'
SITEURL = 'chriscowley.me.uk'
AUTHOR_EMAIL = "chris@chriscowley.me.uk"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_FEED_ATOM = 'feeds/%s.atom.xml'

TRANSLATION_FEED_ATOM = None
THEME = "/home/chris/Development/pelican-themes/pelican-bootstrap3"
BOOTSTRAP_THEME = "yeti"
PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS = [ 'summary', 'gravatar', 'liquid_tags.img', 'liquid_tags.video',
            'pelican_gist', 'liquid_tags.img', 'clean_summary',
            'bootstrapify'
 #           'better_figures_and_images'
          ]
#            'liquid_tags.youtube', 'liquid_tags.vimeo',
#            'liquid_tags.include_code', 'better_figures_and_images' ]

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/')
#         )

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/chriscowleyunix'),
          ('github', 'http://github.com/chriscowley'),)

RESPONSIVE_IMAGES = True
DEFAULT_PAGINATION = 10

STATIC_PATHS = [ 'images', 'assets' ]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

DISQUS_SITENAME = "yetanotherlinuxblog"
GOOGLE_ANALYTICS = "UA-32843690-1"
