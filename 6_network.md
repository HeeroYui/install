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


Corret ontrol of time:
========================

Install servie of network time protocol:

```
pacman -S ntp
```

For ce the time to update fast and not with small change

```
ntpd -qg
```

Start a service:

```
systemctl stop ntpd
```

Display the current status

```
timedatectl status
```
