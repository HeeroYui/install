#!/bin/bash
echo 30 > /sys/devices/system/cpu/intel_pstate/max_perf_pct
echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo

