# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import shutil
import socket
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from util_function import inc_volume
from util_function import dec_volume
from util_function import toggle_mute

mod = "mod4"
terminal = "alacritty"
app_browser = "google-chrome-stable"
app_skype = "skypeforlinux"
app_telegram = "telegram-desktop"


keys = [
    # Application key-binds
    Key([mod], "b", lazy.spawn(app_browser), desc="Launch Google Chrome"),
    Key([mod], "s", lazy.spawn(app_skype), desc="Launch Skype"),
    Key([mod], "t", lazy.spawn(app_telegram), desc="Launch Telegram"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    Key([mod, "shift"], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen",
    ),

    KeyChord([mod], "a", [
        Key([], "s",
            lazy.spawn("steam"),
            desc='Open Steam'
            ),
    ]),

    # Sound management
    Key([], "XF86AudioMute", lazy.function(toggle_mute)),
    Key([], "XF86AudioLowerVolume", lazy.function(dec_volume)),
    Key([], "XF86AudioRaiseVolume", lazy.function(inc_volume))
]

groups = [
    Group("1:DEV", layout="colums"),
    Group("2:WWW", layout="treetab"),
    Group("3:CHAT", layout="colums"),
    Group("4:SYS", layout="colums"),
    Group("5:OPT", layout="treetab")
]

from libqtile.dgroups import simple_key_binder

dgroups_key_binder = simple_key_binder("mod4")

def init_layout_theme():
    return {
            "margin": 0,
            "border_width": 1,
            "border_focus": '#5e81ac',
            "border_normal": '#4c566a'
            }

layout_theme = init_layout_theme()

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(**layout_theme),
    # layout.Matrix(),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(),
    layout.TreeTab(**layout_theme)
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#Colors for the bar
def init_colors():
    return [["#2e3440", "#2e3440"], # color 0  dark grayish blue
            ["#2e3440", "#2e3440"], # color 1  dark grayish blue
            ["#3b4252", "#3b4252"], # color 2  very dark grayish blue
            ["#434c5e", "#434c5e"], # color 3  very dark grayish blue
            ["#4c566a", "#4c566a"], # color 4  very dark grayish blue
            ["#d8dee9", "#d8dee9"], # color 5  grayish blue
            ["#e5e9f0", "#e5e9f0"], # color 6  light grayish blue
            ["#eceff4", "#eceff4"], # color 7  light grayish blue
            ["#8fbcbb", "#8fbcbb"], # color 8  grayish cyan
            ["#88c0d0", "#88c0d0"], # color 9  desaturated cyan
            ["#81a1c1", "#81a1c1"], # color 10 desaturated blue
            ["#5e81ac", "#5e81ac"], # color 11 dark moderate blue
            ["#bf616a", "#bf616a"], # color 12 slightly desaturated red
            ["#d08770", "#d08770"], # color 13 desaturated red
            ["#ebcb8b", "#ebcb8b"], # color 14 soft orange
            ["#a3be8c", "#a3be8c"], # color 15 desaturated green
            ["#b48ead", "#b48ead"]] # color 16 grayish magenta

colors = init_colors()

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widget_defaults = dict(
    font="Ubuntu Nerd Font",
    fontsize=12,
    padding=3,
    background=colors[1],
    foreground=colors[5]
)
extension_defaults = widget_defaults.copy()

########## TOP BAR ################

top_bar = bar.Bar(
            [
                widget.Sep(
                    background=colors[1], #2e3440
                    foreground=colors[5], #d8dee9
                    linewidth=1,
                    padding=10
                ),
                widget.Image(
                    filename="~/.config/qtile/icons/qtilelogo.png",
                    iconsize=8,
                    background=colors[1],
                    mouse_callbacks={'Button1': lambda : qtile.cmd_spawn('rofi -show run')}
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.GroupBox(
                    active=colors[16], #b48ead
                    borderwidth=2,
                    disable_drag=True,
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    hide_unused=False,
                    highlight_method='line',
                    inactive=colors[6], #e5e9f0
                    margin_x=0,
                    margin_y=3,
                    padding_x=5,
                    padding_y=8,
                    rounded=False,
                    this_current_screen_border=colors[14], #ebcb8b
                    urgent_alert_method='line'
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.CurrentLayoutIcon(
                    background=colors[1],
                    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                    foreground=colors[6], #e5e9f0
                    padding=0,
                    scale=0.65
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.CurrentLayout(
                    background=colors[1],
                    font='Ubuntu Bold',
                    foreground=colors[6]
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.Prompt(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.Spacer(),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
#                widget.Volume(
                    #cardid=3,#int(module_and_control[0]),
                    #channel='Speaker'#module_and_control[1]
 #               ),
                widget.PulseVolume(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.KeyboardLayout(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.CapsNumLockIndicator(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.Clock(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format='%a %d, (%B) %H:%M:%S '
                ),
            ],
            22,
            opacity=0.9
        )

######################

##### Bottom bar ######
bottom_bar = bar.Bar(
            [
                widget.WindowName(
                    background=colors[1],
                    foreground=colors[6],
                    font='Ubuntu',
                    fontsize = 12,
                    max_chars=60
                ),
                widget.Spacer(),
                widget.Systray(
                    background=colors[1],
                    icon_size=20,
                    padding=4
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.ThermalSensor(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    update_interval=2
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.Memory(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format="{MemUsed: .0f}{mm}",
                    update_interval=1.0
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.CPU(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format='CPU {load_percent}%',
                    update_interval=1
                ),
                widget.CPUGraph(
                    background=colors[1],
                    foreground=colors[6],
                    graph_color=colors[14]
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text='  '
                ),
                widget.Net(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[5],
                    format='{interface}: {down} ↓ ',
                    interface='all',
                    padding=0
                )
            ],
            22,
            opacity=0.9
        )

screens = [
    Screen(
        top=top_bar,
        bottom=bottom_bar
    ),
    Screen(
        top=bar.Bar([
            widget.GroupBox(),
            widget.WindowName(),
        ], 30)
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

#dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.restart
def cleanup():
    shutil.rmtree(os.path.expanduser('~/.config/qtile/__pycache__'))


@hook.subscribe.startup
def autostart():
    home=os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


#@hook.subscribe.startup_once
#def start_once():
#    home = os.path.expanduser('~')
#    subprocess.call([home + '/.config/qtile/autostart.sh'])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
