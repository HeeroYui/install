Install trash management interface
==================================

Remove the rm command permit to prevent the r=error of reomoving current work element

Install
=======

```
pacman -S trash-cli
```


Configure your bash
===================

edit your bashrc: ```vim ~/.bashrc```

```
# prevent the removing by error
alias rm='echo -e "========================================================\n== You must use trash instead of rm ==> prevent error ==\n========================================================\n"; echo > /dev/null'
```

