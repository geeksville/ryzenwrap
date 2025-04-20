#!/usr/bin/env python3

import sys
import os
import subprocess
import time


def set_gpu_performance_level(mode):
    gpu_path = "/sys/devices/pci0000:00/0000:00:08.1/0000:c4:00.0/power_dpm_force_performance_level"
    try:
        subprocess.run(
            ["sudo", "bash", "-c", f"echo {mode} > {gpu_path}"],
            check=True
        )
        print(f"Setting GPU performance level to {mode}")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to set GPU performance level to {mode}. {e}", file=sys.stderr)


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

    # Power settings based on mode
    if mode_arg == "low":
        norm_lim = 30
        fast_lim = 40
        slow_lim = 20
        gpu_mode = "low"
    elif mode_arg == "powersave":
        norm_lim = 55
        fast_lim = 55
        slow_lim = 40
    elif mode_arg == "balanced":
        norm_lim = 71
        fast_lim = 71
        slow_lim = 52
    elif mode_arg == "high":
        norm_lim = 86
        fast_lim = 86
        slow_lim = 70
    else:
        print(f"Error: Invalid argument '{mode_arg}'. Use 'low/powersave/balanced/high'.", file=sys.stderr)
        sys.exit(1)

    time.sleep(1)  # Wait for 1 second (nasty hack to make sure KDE is done setting things)
    # Call ryzenadj with the calculated limits
    call_ryzenadj([
        f"--stapm-limit={norm_lim * 1000}",
        f"--fast-limit={fast_lim * 1000}",
        f"--slow-limit={slow_lim * 1000}"
    ])

    # Set GPU performance level
    set_gpu_performance_level(gpu_mode)


if __name__ == "__main__":
    main()
