#!/bin/bash
echo 100 > /sys/devices/system/cpu/intel_pstate/max_perf_pct
echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo

