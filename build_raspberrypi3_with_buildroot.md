basis:
======

from: https://code4pi.fr/2014/03/creation-dune-custom-image-pour-votre-raspberry-pi/#more-470

downmload last buildroot version:
```
git clone http://git.buildroot.net/buildroot
# or 
git clone git://git.busybox.net/buildroot
cd buildroot
make raspberrypi3_defconfig
make menuconfig
  toolchain -> Enable stack protection support ==> set at true
make -j8
```

Now the kernel and all that is needed to sater has been created in ```output``` and the bases if images is set in ```output/image```

Now we need to install toolchain and basis headers:

```
expoort TOOLCHAIN_PATH=../generate-toolchain
mkdir -p $TOOLCHAIN_PATH

```
