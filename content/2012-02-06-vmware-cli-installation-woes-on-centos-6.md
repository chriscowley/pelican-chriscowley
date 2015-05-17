title: "VMware CLI installation woes on Centos 6"
date: 2012-02-06 13:09
comments: true



Installing the VMware CLI should have been simple, but it was a bit of a fiddle.

Use yum  all the bits it needs:
<!-- more -->
```
yum install make autoconf automake openssl-devel gcc gcc-c++ make uuid-perl libuuid-devel uuid-devel  perl-Data-Dump perl-SOAP-Lite perl-XML-SAX perl-XML-NamespaceSupport perl-XML-LibXML perl-XML-LibXML-Common perl-CPAN
```

You should now be able to run the installer, but I had another problem though. The installer script would not believe me that I had a direct internet connection and insisted that I gave some proxy server settings. As a simple workaround I just commented out that code in the installation script:
```
if ( direct_command("env | grep -i http_proxy") ) {
 $httpproxy = 1;
} else {
 print wrap("http_proxy not set. please set environment variable 'http_proxy' e.g. export http_proxy=https://myproxy.mydomain.com:0000 . \n\n", 0);
}
if ( direct_command("env | grep -i ftp_proxy") ) {
 $ftpproxy = 1;
} else {
 print wrap("ftp_proxy not set. please set environment variable 'ftp_proxy' e.g. export ftp_proxy=https://myproxy.mydomain.com:0000 . \n\n", 0);
}

if ( !( $ftpproxy && $httpproxy)) {
    uninstall_file($gInstallerMainDB);
    exit 1;
}
```
After this I was able to run the installer with no problems. Of course, there is still the problem I have VMware about them putting their files under _/usr_. If it is not under control of my package manager, the default should be _/opt_ or _/usr/local_.

