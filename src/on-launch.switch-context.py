#!/usr/bin/env python3
import os
import configparser
from subprocess import PIPE, run
from sys import platform

CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'ssid_context_map.ini')


def main():
    ssid_context_map = read_config()
    if ssid_context_map is None:
        return
    ssid = get_ssid()
    if ssid is None:
        return
    if ssid in ssid_context_map:
        context = ssid_context_map[ssid]
        current_context = get_current_context()
        if current_context != context:
            set_context(context)
            print('Set context "{0}", because of WiFi SSID "{1}"'.format(context, ssid))


def get_task_command():
    return ['task', 'rc.hooks=off']


def get_current_context():
    return run(get_task_command() + ['_get', 'rc.context'], stdout=PIPE).stdout.strip().decode('ascii') or 'none'


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_NAME, encoding='utf-8')
    data = config['DEFAULT']
    ssid_context_map = {}
    for context in data:
        for ssid in data[context].split(','):
            ssid = ssid.strip()
            if ssid:
                ssid_context_map[ssid] = context
    return ssid_context_map


def set_context(context):
    run(get_task_command() + ['context', context])


def get_ssid_macosx():
    cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
    for row in run([cmd, '-I'], stdout=PIPE, encoding='utf-8').stdout.split("\n"):
        key, val = [x.strip() for x in row.split(':', 1)]
        if key == 'SSID':
            return val
    return None


def get_ssid_windows():
    return None


def get_ssid_linux():
    return None


def get_ssid():
    if platform == 'darwin':
        return get_ssid_macosx()
    else:
        return None
        # if platform.startswith('linux'):
        # elif platform.startswith('win32'):
        # elif platform.startswith('cygwin'):
        # elif platform.startswith('darwin'):
        # elif platform.startswith('os2'):
        # elif platform.startswith('os2emx'):
        # elif platform.startswith('riscos'):
        # elif platform.startswith('atheos'):


if __name__ == '__main__':
    main()
