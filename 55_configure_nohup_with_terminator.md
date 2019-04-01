Configure nohup with terminator:
================================


you need to edit the terminator config and add this 

edn .config/terminator/config

```
[global_config]
  dbus = False
```


now you can change user and execute

```
nohup terminator&
```

