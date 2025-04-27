#!/usr/bin/env python3

import sys
import os
import subprocess
import time


def sudo_echo(filename, contents):
    try:
        print(f"Setting {filename} to {contents}")        
        subprocess.run(
            ["sudo", "bash", "-c", f"echo {contents} > {filename}"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: Can't set {filename} to {contents} {e}", file=sys.stderr)


def set_gpu_performance_level(mode):
    sudo_echo("/sys/devices/pci0000:00/0000:00:08.1/0000:c4:00.0/power_dpm_force_performance_level", mode)


# for asys-wmi
# /sys/devices/platform/asus-nb-wmi/throttle_thermal_policy
# 0 - default, 1 - overboost, 2 - silent
def set_asus_thermal_policy(mode):
    sudo_echo("/sys/devices/platform/asus-nb-wmi/throttle_thermal_policy", mode)

def call_ryzenadj(arguments):
    # Check ~/.local/bin/ryzenadj
    ryzenadj_path = os.path.expanduser("~/.local/bin/ryzenadj")
    if not os.path.isfile(ryzenadj_path):
        # Check /usr/sbin/ryzenadj
        ryzenadj_path = "/usr/sbin/ryzenadj"
        if not os.path.isfile(ryzenadj_path):
            print("Error: RyzenAdj not found in ~/.local/bin or /usr/sbin.", file=sys.stderr)
            sys.exit(1)

    # Execute ryzenadj with the provided arguments
    try:
        subprocess.run([ryzenadj_path] + arguments, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: RyzenAdj command failed with error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ryzen-wrap.py <low/powersave/balanced/high>")
        sys.exit(1)

    mode_arg = sys.argv[1]

    # Default GPU mode
    gpu_mode = "auto"

    # for asys-wmi
    # /sys/devices/platform/asus-nb-wmi/throttle_thermal_policy
    # 0 - default, 1 - overboost, 2 - silent
    ASUS_DEFAULT = 0
    ASUS_OVERBOOST = 1
    ASUS_SILENT = 2

    asus_mode = ASUS_DEFAULT

    if mode_arg == "low":
        fast_lim = 40
        slow_lim = 20
        gpu_mode = "low"
        asus_mode = ASUS_SILENT
        opts = ["--power-saving"]
    elif mode_arg == "powersave":
        # This is the same as low, but with a different GPU mode
        fast_lim = 55
        slow_lim = 40
        asus_mode = ASUS_SILENT
        opts = ["--power-saving"]
    elif mode_arg == "balanced":
        fast_lim = 71
        slow_lim = 52
        opts = ["--max-performance"]
    elif mode_arg == "high":
        fast_lim = 86
        slow_lim = 70
        asus_mode = ASUS_OVERBOOST
        opts = ["--max-performance"]
    else:
        print(f"Error: Invalid argument '{mode_arg}'. Use 'low/powersave/balanced/high'.", file=sys.stderr)
        sys.exit(1)

    time.sleep(1)  # Wait for 1 second (nasty hack to make sure KDE is done setting things)
    set_asus_thermal_policy(asus_mode)

    # Call ryzenadj with the calculated limits
    opts += [
        f"--fast-limit={fast_lim * 1000}",
        f"--slow-limit={slow_lim * 1000}"
    ]
    # no longer needed - better to just use the Asus API
    # call_ryzenadj(opts)



    # Set GPU performance level
    set_gpu_performance_level(gpu_mode)


if __name__ == "__main__":
    main()
