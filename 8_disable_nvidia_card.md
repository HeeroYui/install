Disable the nvidia 'nouveau driver'
===================================

see

https://askubuntu.com/questions/841876/how-to-disable-nouveau-kernel-driver


just do:
========

According to the NVIDIA developer zone: Create a file
```
nano /etc/modprobe.d/blacklist-nouveau.conf
```

with the following contents:
```
blacklist nouveau
options nouveau modeset=0
```

Regenerate the kernel initramfs:
```
sudo update-initramfs -u
```

and finally: reboot
```
shutdown -r now
```

Read more at: http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ixzz4rQODN0jy

