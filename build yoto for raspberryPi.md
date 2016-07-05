Raspberry Pi with Yocto
=======================

Install dependency:
```
su
pacman -S diffstat chrpath cpio
exit
```

configure locals:
```
su
locale -a
edn /etc/locale.gen
  unselect at minimum en_US.UTF-8 UTF-8
locale-gen
exit
```

1) set-up working directory:
----------------------------

```
mkdir -p RASPBERRYPI/BSP
cd RASPBERRYPI/BSP
```

2) Clone of Yocto:
------------------

```
git clone -b krogoth git://git.yoctoproject.org/poky.git
cd poky/
```

3) Clone of meta de Raspberry Pi:
---------------------------------

```
git clone -b master git://git.yoctoproject.org/meta-raspberrypi
```

4) Clone of meta Open Embedded:
-------------------------------

```
git clone -b krogoth https://github.com/openembedded/meta-openembedded.git
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

Open: ```conf/local.conf```

find: ```MACHINE ??= "qemux86"```

Remplace with: ```MACHINE ?= "raspberrypi2"```

find: ```PACKAGE_CLASSES ?= "package_rpm"```

Remplace with: ```PACKAGE_CLASSES ?= "package_deb"```



Add at the end:
```
BBMASK = "meta-raspberrypi/recipes-multimedia/libav|meta-raspberrypi/recipes-core/systemd"
```

Open: ```conf/bblayers.conf```

find:
```
BBLAYERS ?= " \
  ${HOME}/RASPBERRYPI/BSP/poky/meta \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-yocto \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-yocto-bsp \
  "
```

Remplace with:
```
BBLAYERS ?= " \
  ${HOME}/RASPBERRYPI/BSP/poky/meta \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-yocto \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-yocto-bsp \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-raspberrypi \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-openembedded/meta-oe \
  ${HOME}/RASPBERRYPI/BSP/poky/meta-openembedded/meta-networking \
  "
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

some yocto options:
===================
in the file: ```conf/local.conf```
# mumber of distinct lib to compile at the same time
BB_NUMBER_THREADS = "4"
# number of thread fore eache build
PARALLEL_MAKE = "-j 4"


============
