gui
---
```
pacman -S cinnamon
```

set auto-start
--------------
```
# when no graphic engine
echo \#exec cinnamon-session-cinnamon2d > ~/.xinitrc
# With graphic engine
echo exec cinnamon-session >> ~/.xinitrc
```

other gui tools
---------------
```
# for open archive in gui
pacman -S cfile-roller
```

Check the Cart graphic corectly install
---------------------------------------
```
# list the output card : (permit to know wich graphic ard we have)
lspci | grep VGA
# install all the graphic card drivers:
pacman -S xorg xorg-drivers
# restart computer
# ...
# install bench tool
pacman -S virtualgl
# run sample:
glxspheres64
# here we will know how the graphic interfae is run
```
