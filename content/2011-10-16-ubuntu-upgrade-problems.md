Title: Ubuntu upgrade problems
comments: true
categories: linux

Usually the release upgrade is relatively trouble-free, but this time I had a minor problem. After the upgrade I had no X Windows. It turned out that the NVidia driver not loading.

I had to boot it up in rescue mode, which is selectable from the Grub menu. From there I could drop to a root console.

The first step is to remount / as read-write and then mount my boot partition (/dev/sda1).
```
mount -o rw,remount /
mount /dev/sda1 /boot
```
Now I just need to move the xorg.conf to one side and reinstall the nvidia driver
```
mv /etc/X11/xorg.conf /etc/X11/xorg.conf.bak
apt-get remove nvidia-current && apt-get install nvidia-current
```
After a reboot it should come up all fine and dandy.

