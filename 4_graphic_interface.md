Set first the Xautority:

```
touch ~/.Xauthority
```

Configure Xlayout in french:

'''
vim "/etc/X11/xorg.conf.d/00-keyboard.conf"
'''

'''
Section "InputClass"
    Identifier         "Keyboard Layout"
    #MatchIsKeyboard    "yes"
    Option             "XkbLayout"  "fr"
    Option             "XkbVariant" "latin9"
EndSection
'''
gui
---
```
pacman -S cinnamon
```
OR
---
```
pacman -S awesome xlockmore archlinux-xdg-menu
```
```xlockmore``` ==> run xlock to lock the screen
```archlinux-xdg-menu``` ==> setup a generic menu

set auto-start
--------------
```
# when no graphic engine
echo \#exec cinnamon-session-cinnamon2d > ~/.xinitrc
# With graphic engine
echo exec cinnamon-session >> ~/.xinitrc
```
OR
```
# when no graphic engine
echo \#exec awesome > ~/.xinitrc
```

other gui tools
---------------
```
# for open archive in gui
###### pacman -S cfile-roller
# file explorer
pacman -S thunar
```


Check the Card graphic corectly install
---------------------------------------
```
# list the output card : (permit to know wich graphic ard we have)
lspci | grep VGA
# install all the graphic card drivers:
pacman -S xorg xorg-xinit
# restart computer
# ...
# install bench tool
pacman -S virtualgl
# run sample:
glxspheres64
# here we will know how the graphic interfae is run
```


Start automaticly the X when first log
---------------------------------------
```
# start X
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx
# force lang of output in english ==> better for developpement
LANG=en_US.UTF-8
```

Configure awesome:
------------------

base:
```
mkdir ~/.config/awesome
cp /etc/xdg/awesome/rc.lua ~/.config/awesome/
```

Create the menu:
```
xdg_menu --format awesome --root-menu /etc/xdg/menus/arch-applications.menu >~/.config/awesome/archmenu.lua
```

And Add in rc.lua:
```
xdg_menu = require("archmenu")

mymainmenu = awful.menu({ items = { { "awesome",      myawesomemenu, beautiful.awesome_icon },
                                    { "Applications", xdgmenu },
                                    { "Terminator",   "terminator",  "/usr/share/icons/hicolor/16x16/apps/terminator.png" },
                                    { "Opera",        "opera",       "/usr/share/icons/hicolor/16x16/apps/opera.png" },
                                    { "Chromium",     "chromium",    "/usr/share/icons/hicolor/16x16/apps/chromium.png" },
                                    { "Thunar",       "thunar" },
                                    { "Edn",          "edn",         "/home/edupin/.local/application/edn.app/share/edn/icon.png"},
                                    { "X-lock",       "xlock"}
                                  }
                        })
```

Add a shortcut to lock screen
```
-- {{{ Key bindings
globalkeys = awful.util.table.join(
    awful.key({ modkey,           }, "z",      function () awful.util.spawn("xlock") end), -- this to add
```






