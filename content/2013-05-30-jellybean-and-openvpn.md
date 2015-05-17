title: "Jellybean and OpenVPN"
date: 2013-05-30 22:14
comments: true
{% img right https://openvpn.net/templates/telethra/img/ovpntech_logo-s.png %}Setting up the server is well documented elsewhere, the [official howto](https://openvpn.net/index.php/open-source/documentation/howto.html#quick) works nicely for me. I use a Virtual TUN network (routed) with clients connecting via UDP 1194, with all the network config pushed out by the server. Follow the howto and you will get that at the end.
<!-- more -->

When you create the key for your Jellybean client, create a PKCS12 certificate. This just means using the `build-key-pkcs12` script instead of `build-key`. Copy that .p12 key to the root of the SD card in your phone. 

Now you can make that certificate available for use by the OpenVPN client. Open *Setting -> Security -> Install from SD Card* and choose the .p12 file you just copied there.

Install [OpenVPN for Android/ICS-openvpn](https://code.google.com/p/ics-openvpn/). In that create a new profile with a suitable name. Under "Basic" configure the *Server Address* and choose your certificate.

The end...
