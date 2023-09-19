#!/usr/bin/python3

import json
import subprocess

def disable_scr():
    subprocess.run('xrandr --output DVI-I-1-1 --off', shell=True)
    subprocess.run('xrandr --output DVI-I-2-2 --off', shell=True)

def enable_scr():
    subprocess.check_output('bash /home/nao/.Informatique/Informatique/IDE/ArkSL/triple-screens.sh', shell=True)

def ws_backup():
    backup = []
    i3ws = 'i3-msg -t get_workspaces'
    cmd = subprocess.check_output(f'{i3ws}', shell=True).decode()
    ws_all = json.loads(cmd)
    for ws in ws_all:
        ws_name = ws["name"]
        ws_out = ws["output"]
        ws_dict = {ws_name: ws_out}
        backup.append(ws_dict)
#    print(backup)
    return backup

def ws_restore(ws_keep):
    # i3-msg 'workspace number 8; move workspace to output eDP-1'
    i3restore = "i3-msg 'workspace number 8; move workspace to output eDP-1'"
    for ws in ws_keep: # ws_keep est une variable initialisee dans __init__() self.ws_keep
        for k, v in ws.items():
            try:
                subprocess.check_output(f"i3-msg 'workspace number {k}; move workspace to output {v}'", shell=True)
            except:
                pass

if __name__ == '__main__':
    ws_keep = ws_backup()
    ws_restore()
    
