import logging
import re
import os
import subprocess

logging.basicConfig(filename="audio_catch.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

available_controls = ['Master', 'Speaker']

def get_module_number():
    with open("/proc/asound/modules", "r") as f:
        lines = f.readlines()

    return_results = list()

    for line in lines:
        module_tuple = line.split()
        if "usb" in module_tuple[1]:
            return_results.append(module_tuple[0])
    if not return_results:
        return_results = ['0']
    logging.info(f"Module_numbers: {return_results}")
    return return_results

def get_scontrol_name(module_numbers):
    result = ("0", "Master")
    for mn in module_numbers:
        stdout = subprocess.run(['amixer', '-c', mn],
                            capture_output=True,
                            shell=False)
        # name_line = stdout.stdout.decode('utf-8').split('\n')[0]
        # logging.info(f"Control Name: {name}")
        amixer_result = stdout.stdout.decode('utf-8')
        names = re.findall(r"'(.*?)'", amixer_result)
        for name in names:
            if name in available_controls:
                result = (mn, name)
    logging.info(f"Module number and control name: {result}")
    return result

ICON_DIR = '/usr/share/archcraft/icons/dunst'
NOTIFY_CMD = 'dunstify -u low -h string:x-dunst-stack-tag:obvolume'
MUTED = 1
UNMUTED = 0

def get_volume():
    cmd_call = subprocess.run(['pulsemixer', '--get-volume'], capture_output=True)
    volume = cmd_call.stdout.decode('utf-8').split(' ').pop()
    return int(volume)

def get_icon():
    current = get_volume()
    if current == 0:
        return f"{ICON_DIR}/volume-mute.png"
    elif current > 0 and current <= 30:
        return f"{ICON_DIR}/volume-low.png"
    elif current > 30 and current <= 60:
        return f"{ICON_DIR}/volume-mid.png"
    elif current > 60 and current <= 100:
        return f"{ICON_DIR}/volume-high.png"

def notify_user():
    os.system(f"{NOTIFY_CMD} -i {get_icon()} 'Volume : {get_volume()}'")

def get_mute():
    cmd_call = subprocess.run(['pulsemixer', '--get-mute'], capture_output=True)
    mute_state = int(cmd_call.stdout.decode('utf-8'))
    return mute_state

def unmute():
    os.system(f"pulsemixer --unmute")

def mute():
    os.system(f"pulsemixer --mute")

def do_toggle_mute():
    os.system(f"pulsemixer --toggle-mute")

def change_volume(n):
    os.system(f"pulsemixer --max-volume 100 --change-volume {n}")

def inc_volume(qtile):
    if get_mute() == MUTED:
        unmute()
    change_volume('+5')
    notify_user()

def dec_volume(qtile):
    if get_mute() == MUTED:
        unmute()
    change_volume('-5')
    notify_user()

def toggle_mute(qtile):
    if get_mute() == MUTED:
        do_toggle_mute()
        os.system(f"{NOTIFY_CMD} -i {ICON_DIR}/volume-mute.png 'Mute'")
    else:
        do_toggle_mute()
        current_volume_icon = get_icon()
        os.system(f"{NOTIFY_CMD} -i {current_volume_icon} 'Unmute'")

