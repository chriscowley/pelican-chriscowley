---
layout: post
title: "In praise of old school UNIX"
date: 2013-02-05 16:13
comments: true
categories: linux
---
What am I doing today? Documentation that is what. I am writing a document on how to do [this](http://www.chriscowley.me.uk/blog/2012/11/19/sftp-chroot-on-centos/). To any Linux user it is a very simple process and I could just give them a link to my own website.
<!--more-->

I am not writing this for a techinical audience though. The people who are going to perform this work will be the 'Level 1 operatives'. This translates roughly to "anyone we can find on the street corners of some Far East city". If I tell them to press the red button labelled "press me" and it turns out to be orange, they will stop. I cannot assume the ability to edit a file in Vi. How can you work around this, well you need to make everything a copy and paste operation. This is easily done in Bash thanks to IO redirection and of course Sed.

Now, a brief recap may be in order, as there are some perfectly knowledgable Linux users who do not know what Sed is. Really, one of them sits behind me. Sed stands for Stream EDitor, and it parses text and applies transformations to it. It was one of the first UNIX utilities. It kind of sits between [Grep](https://en.wikipedia.org/wiki/Grep) and [Awk](https://en.wikipedia.org/wiki/AWK_programming_language) and is [surprisingly powerful](http://uuner.doslash.org/forfun/).

Anyway, I need to edit a line in a file then add a block of code at the end.

```
cp -v /etc/ssh/sshd_config{,.dist}
sed -i ''/^Subsystem/s#/usr/libexec/openssh/sftp-server#internal-sftp#g' \ 
    /etc/ssh/sshd_config
```

First line obviously is a contracted cp line which puts the suffix *.dist* on the copy.

The basic idea is that it runs through the file (/etc/ssh/sshd_config) and looks for any line that starts with "Subsystem" (`/^Subsystem/`). If it finds a line that matches it then will perform a "substituion" (`/s#`). The next 2 blocks tell it what the substitution will be in the order "#From#To#". The reason for  the change from `/` to `#` is because of the / in the path name (thanks to [Z0nk](http://www.reddit.com/user/z0nk)  for reminding me that you can use arbitary seperators). The "#g" tells Sed to perform the substituion on every instance it finds on the line, rather than just the first one. It is completely superfluous in this example, but I tend to put it in from force of habit. Finally the "-i" tells Sed to perform the edit in place, rather than outputing to Stdout.

The next bit is a bit cleverer. With a single command I want to add a block of text to the file.

```
cat <<EOF | while read inrec; do echo $inrec >> /etc/ssh/sshd_config; done
Match Group transfer
ChrootDirectory /var/local/
ForceCommmand internal-sftp
X11Forwarding no
AllowTcpForwarding no

EOF
```

Here `cat <<EOF` tells it send everything you type to Stdout until it sees the string EOF. This then gets piped to a `while` loop that appends each line of that Stdout to the file we want to extend (_/etc/ssh/sshd_config_ in this case).

Using these old tools and a bit of knowledge of how redirection works has enabled me to make a document that anyone who can copy/paste can follow. It is very easy for technical people to forget that not everyone has the knowledge we have. To us opening Vi is perfectly obvious, but to others maybe it isn't and they are not being paid enough to know. They are just being paid to follow a script. I may not like it, but it is the case - it also helped turn a boring documentation session into something a little more interesting. Which is nice!
