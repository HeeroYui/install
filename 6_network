Acces at the bonjour methodologie:
==================================


Install avahi lib to access at bonjour:
```
pacman -S avahi
```

Install the interface with the libC to acces exter elements
```
pacman -S nss-mdns
```

Configure the search element for ethernel/internet
```
vim /etc/nsswitch.conf
```
	Add mdns (search in ipv4 and ipv6)
	-> hosts: files dns myhostname mdns
```
sync
```

Start avaki deamon:
```
systemctl enable avahi-daemon.service
systemctl start avahi-daemon.service
```

