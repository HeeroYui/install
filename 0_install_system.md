My install and configuration script for Archlinux.

see: https://www.tecmint.com/arch-linux-installation-and-configuration-guide/

Archlinux Install
=================

Create USB
----------
```
dd if=*.iso of=/dev/sdb
```

Init
----
```
loadkeys fr-latin9
wifi-menu
```

Prepare the storage devices
---------------------------

mettre ma partition en ```GPT```

```
fdisk
=> m
```


```
cfdisk /dev/sda
```

| Name | Boot  | Size   | Format     | Mount |
| ---- | :---: | -----: | :--------: | ----- |
| sda1 | *     | 300M   | mkfs.fat   | /boot | EFI System
| sda2 |       | 8G     | mkswap     |       | swap
| sda3 |       | 32G    | mkfs.ext4  | /     | linux filesystem
| sda4 |       | ALL    | mkfs.ext4  | /home | linux home

mkfs all...  
```
mkfs.fat -F32 /dev/sda1
mkswap /dev/sda2
mkfs.ext4 /dev/sda3
mkfs.ext4 /dev/sda4

```

mount all...  
```
mount /dev/sda3 /mnt  
mkdir /mnt/{boot,home}  
mount /dev/sda1 /mnt/boot  
mount /dev/sda4 /mnt/home  
swapon /dev/sda2  
```
Install the base system
-----------------------
Replace \<foobar\> by what you want...
```
pacstrap /mnt base base-devel syslinux vim git gptfdisk
genfstab -L -p /mnt >> /mnt/etc/fstab  
arch-chroot /mnt  
echo <laptop-name> > /etc/hostname  
ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime  
vim /etc/locale.gen (en_us, fr, ja & utf-8)  
locale-gen  
echo "LANG=\"en_US.UTF-8\"" > /etc/locale.conf  
echo "KEYMAP=<fr-latin9/jp106>" > /etc/vconsole.conf  

mkinitcpio -p linux  
syslinux-install_update -iam
```
then edit /boot/syslinux/syslinux.cfg if /dev/sda3 is not correct  

Pacman...  
activate Color and multilib in /etc/pacman.conf

Wireless network configuration
------------------------------
```
pacman -S networkmanager  
systemctl enable NetworkManager.service  
```
list network: nmcli con show  
connect to network: nmcli dev wifi connect <name> password <password> [iface wlan1]  
or use the ncurse ui tool "nmtui"

Archlinux package config
------------------------

install all package you want

User Configuration
==================

Change Root pasword
-------------------
```
passwd
```

Adding User
-----------
```
useradd -g users -m -s /bin/bash <username>  
```
Adding user to a group:  
```
usermod -a -G <wheel,audio,video,disk,storage> <username>  
```
Change pasword:
```
passwd <username>
```

Misc
====


X Server multi-user
-------------------
Edit /etc/pam.d/su su-l and add:  
```
session        optional        pam_xauth.so
```

Printer Management
------------------
```
pacman -S --needed cups ghostscript hplip
systemctl enable cups
systemctl start cups
```
Then add printer HP PhotoSmart 6520 using http://localhost:631/ discover network  
note use hpcups over hpijs to get border printed   

Disable laptop lid switch handle (usefull when using external screen)
---------------------------------------------------------------------
Edit /etc/systemd/logind.conf and enable:  
```
LidSwitchIgnoreInhibited=yes
```

Restart computer....
