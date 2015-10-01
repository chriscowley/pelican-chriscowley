PyCurl and self-signed SSL certificates
#######################################
:tags:  Programming

At Snell we make heavy use of self-signed certificates for internal
websites, such as the R&D wiki. Active Directory makes it easy for us to
make this transparent to the users, those that use Firefox/Chrome can
find our well-published instructions to add the CA certificate to their
own browsers.

Today I was writing a script to that pulls lots of attachments off our
Confluence wiki, which we access through SSL using one of those
certificates. Of course PyCurl moaned that it could not verify the host,
but I did not care – I know it is the right host!

Finding documentation both on SSL and PyCurl is problematic at best.
OpenSSL’s documentation it complete, but could not be more unreadable if
written by a right-handed doctor using a broken crayon with his
left-hand; pyCurl’s documentation is non-existent.

After an hour of Google-Fu and DuckDuckGo-Fu I finally managed to do
what I wanted:

::

    #!/usr/bin/env python
    downloadedFile = "/tmp/stuff"
    outfile = file(downloadedFile, 'wb')
    url = https://someurl.example.com
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
    c.setopt(c.WRITEFUNCTION, outfile.write)
    c.setopt(c.SSL_VERIFYPEER, 0) # That is you key line for this purpose!
    c.perform()
    c.close

There you go!
