#!/bin/sh

picom --config ~/.config/picom/picom.conf -b &
nitrogen --restore &
xrandr --output DP-3 --auto --output HDMI-0 --auto --below DP-3 &
