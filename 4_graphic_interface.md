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
---
```
# for open archive in gui
pacman -S cfile-roller
```
