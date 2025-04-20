# ryzen-wrap

This is a little yucky python script which sets an Asus Flow Z13 2025 (Strix Halo 395+ APU) to run at various TDP levels. It has no GUI
and uses the ryzenadj tool to do its work. It also sets the GPU into a very low power mode (saves 3-5W!) if you select the "low"/silent
power setting.

Eventually you'll want the [official version](https://github.com/FlyGoat/RyzenAdj), but if you are using this
script right now you can use my [fork](https://github.com/geeksville/RyzenAdj).

Since this script is crude right now, it assumes you have that tool installed in ~/.local/bin or /usr/sbin.

## Usage

ryzen-wrap.py <low/powersave/balanced/high>

