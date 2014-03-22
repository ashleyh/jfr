#!/usr/bin/env python2

from __future__ import print_function

import argparse
import os
import sys
import runpy
import urllib
import subprocess


def die(*args):
    print('Error:', *args, file=sys.stderr)
    sys.exit(1)


def check_is_script(path):
    if not os.path.exists(path):
        die(path, 'does not exist')


def get_cache_home():
    xdg_cache_home = os.getenv('XDG_CACHE_HOME')
    if xdg_cache_home is None:
        home = os.path.expanduser('~')
        return os.path.join(home, '.cache')
    else:
        return xdg_cache_home


def get_venv_name(script_path):
    real_path = os.path.realpath(script_path)
    return urllib.quote(real_path, safe='')


def get_venv_path(script_path):
    jfr_home = os.path.join(get_cache_home(), 'jfr')
    venv_name = get_venv_name(script_path)
    return os.path.join(jfr_home, venv_name)


def create_venv_if_missing(venv_path):
    if os.path.exists(venv_path):
        return
    subprocess.call(['virtualenv', venv_path])


def activate_venv(venv_path):
    activator = os.path.join(venv_path, 'bin', 'activate_this.py')
    execfile(activator, dict(__file__=activator))


def install_requirements(script_path, venv_path):
    requirements_path = os.path.join(
        os.path.dirname(script_path), 'requirements.txt')
    if os.path.exists(requirements_path):
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        subprocess.call([pip_path, 'install', '-r', requirements_path])


def setup_venv(script_path):
    venv_path = get_venv_path(script_path)
    create_venv_if_missing(venv_path)
    install_requirements(script_path, venv_path)
    activate_venv(venv_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    check_is_script(args.path)
    setup_venv(args.path)
    runpy.run_path(args.path)


if __name__ == '__main__':
    main()
