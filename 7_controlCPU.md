CPU can be downgraded to reduce fan noise
=========================================

For this you have tools

Disable intel burst
```
echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo
```

Force the CPU to not upper a frequency:
```
echo 30 > /sys/devices/system/cpu/intel_pstate/max_perf_pct
```

you can check the all values with :
```
cat /sys/devices/system/cpu/intel_pstate/*
```

you can check you CPU frequency with:
```
cat /proc/cpuinfo | grep MHz
```

you can check :

https://wiki.archlinux.org/index.php/CPU_frequency_scaling