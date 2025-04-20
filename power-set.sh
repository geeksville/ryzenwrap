set -e

# Script to control AMD GPU power mode

if [ -z "$1" ]; then
  echo "Usage: $0 <low/powersave/balanced/high>"
  exit 1
fi

mode_arg="$1"

RYZENADJ_PATH="/home/kevinh/.local/bin/ryzenadj"

# GPUMODE or performance, defaults to "auto"
GPUMODE="auto"

case "$mode_arg" in
  "low") # A Very low setting for max power savings, runs GPU clocks quite slow
    NORM_LIM="55"
    FAST_LIM="55"
    SLOW_LIM="40"
    GPUMODE="low"
    ;;
  "powersave") # Decent GPU, same CPU settings as normal BIOS "power save" mode
    NORM_LIM="55"
    FAST_LIM="55"
    SLOW_LIM="40"
    ;;
  "balanced") # Decent GPU, same CPU settings as normal BIOS "balanced" mode
    NORM_LIM="71"
    FAST_LIM="71"
    SLOW_LIM="52"
    ;;
  "high") # Decent GPU, same CPU settings as normal BIOS "performance" mode
    NORM_LIM="86"
    FAST_LIM="86"
    SLOW_LIM="70"
    ;;    
  *)
    echo "Error: Invalid argument '$mode_arg'. Use 'low/powersave/balanced/high'."
    exit 1
    ;;
esac

$RYZENADJ_PATH --stapm-limit 55000 --fast-limit 55000 --slow-limit 40000

# When laptop is under low load, neither of the following to techniques save power

# Example: Disable the last 16 cores(useful for disabling the SMT threads or the second half of cores)
# echo "Attempting to disable hyperthread 'cores' FIXME verify if this saves power"
# for i in {16..31}; do
#  sudo sh -c "echo 0 > /sys/devices/system/cpu/cpu$i/online"
# done

# echo "Setting last 8 cores to very low max speed' FIXME me verify if this saves power"
# for i in {8..15}; do
#  sudo cpupower -c $i frequency-set -r -u 600000
# done

# saves 3W!
echo "Setting GPU performance level to $GPUMODE"
sudo bash -c "echo $GPUMODE > /sys/devices/pci0000:00/0000:00:08.1/0000:c4:00.0/power_dpm_force_performance_level"

# Note: external system draw (screen, RAM etc) when CPU is not very busy is about 3W, but can be as high as 5W
# In lowest power mode the total system draw is about 10W

# Show status
# lscpu --all --extended
