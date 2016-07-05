Raspberry Pi with Yocto
=======================

1) set-up working directory:
----------------------------

```
mkdir -p RASPBERRYPI/BSP
cd RASPBERRYPI/BSP
```

2) Clone of Yocto:
------------------

```
git clone -b dora git://git.yoctoproject.org/poky.git
cd poky/
```

3) Clone of meta de Raspberry Pi:
---------------------------------

```
git clone -b dora https://github.com/djwillis/meta-raspberrypi.git
```

4) Clone of meta Open Embedded:
-------------------------------

```
git clone -b dora https://github.com/openembedded/meta-openembedded.git
```

5) Force python 2.7:
--------------------

```
mkdir pythonBase2
cd pythonBase2
ln -s /usr/bin/python2.7 python
ln -s /usr/bin/python2.7-config python-config
export PATH=`pwd`:$PATH
cd ..
```

6) Initialize the configuration:
--------------------------------

```
source oe-init-build-env raspberryPiBuild/
```

7) update configuration file:
-----------------------------

Open: ```local.conf```

find: ```MACHINE ??= "qemux86"```

Remplace with: ```MACHINE ?= "raspberrypi"```

find: ```PACKAGE_CLASSES ?= "package_rpm"```

Remplace with: ```PACKAGE_CLASSES ?= "package_deb"```



Add at the end:
```
BBMASK = "meta-raspberrypi/recipes-multimedia/libav|meta-raspberrypi/recipes-core/systemd"
BBMASK = "meta-raspberrypi/recipes-multimedia/libav|meta-raspberrypi/recipes-core/systemd"
```

Open: ```conf/bblayers.conf```

find:
```
BBLAYERS ?= " \
  /home/util01/RASPBERRYPI/BSP/poky/meta \
  /home/util01/RASPBERRYPI/BSP/poky/meta-yocto \
  /home/util01/RASPBERRYPI/BSP/poky/meta-yocto-bsp \
  "
```

Remplace with:
```
BBLAYERS ?= " \
  /home/util01/RASPBERRYPI/BSP/poky/meta \
  /home/util01/RASPBERRYPI/BSP/poky/meta-yocto \
  /home/util01/RASPBERRYPI/BSP/poky/meta-yocto-bsp \
  /home/util01/RASPBERRYPI/BSP/poky/meta-raspberrypi \
  /home/util01/RASPBERRYPI/BSP/poky/meta-oe/meta-oe \
```

8) Build basic image:
---------------------

Simply run:
```
bitbake core-image-minimal
```

display result:
```
ls -l tmp/deploy/images/raspberrypi/
```

10) Burn image on the sd card:
------------------------------

```
cd tmp/deploy/images/raspberrypi/
sudo dd bs=1M if=core-image-minimal-raspberrypi.rpi-sdimg of=/dev/mmcblk0
```

11) All is ready:
-----------------

login: ```root```
pasword ```root```
