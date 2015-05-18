Skype video on Fedora 64bit
###########################
:tags:  linux

Install Skype – I used these instructions. This will seem to get
everything working, but video will just give you a black screen and no
error message. This is because Skype is 32 bit and your webcam driver is
64 bit. Make sure you have libv4l.i686 installed along with a couple of
other dependencies:

::

    sudo yum install libv4l.i686 alsa-lib.i686 libXv.i686 libXScrnSaver.i686 \
        qt.i686 qt-x11.i686    

Now create a wrapper script to launch it with a custom environment. I
put it in */usr/local/bin/skype*

{% include\_code lang:bash skype %}

This will now get loaded before the main Skype executable and you will
have a working video device.
