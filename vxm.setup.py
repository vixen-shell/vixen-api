"""
Author            : Nohavye
Author's Email    : noha.poncelet@gmail.com
Repository        : https://github.com/vixen-shell/vixen-client.git
Description       : vxm setup file.
License           : GPL3
"""

import os
from subprocess import run, PIPE

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
VXENV_PATH = '/opt/vixen-env'

feature = {
    'name': 'Vixen API'
}

library = {
    'name': 'vixen_api_lib',
    'source': f'{VXENV_PATH}/bin/activate'
}
library['install_command'] = f"source {library['source']} && sudo pip install --upgrade pip && sudo pip install {CURRENT_PATH}"
library['remove_command'] = f"source {library['source']} && sudo pip uninstall {library['name']} --yes"

def package_exist(name: str) -> bool:
    result = run(f"source {library['source']} && pip show {name}", shell=True, stdout=PIPE, stderr=PIPE)
    if result.returncode == 0: return True
    return False

setup = {
    'purpose': f"Install {feature['name']}",
    'tasks': [
        {
            'purpose': f"Install {library['name']} library",
            'process_command': library['install_command'],
            'requirements': [
                {
                    'purpose': 'Check Vixen environment installation',
                    'callback': lambda: os.path.isdir(VXENV_PATH),
                    'failure_details': 'Vixen Environment was not found'
                },
                {
                    'purpose': 'Check an existing library installation',
                    'callback': lambda: not package_exist(library['name']),
                    'failure_details': f"{feature['name']} is already installed"
                }
            ]
        },
        {
            'purpose': 'Remove build folders',
            'process_command': f"sudo rm -r {CURRENT_PATH}/build && sudo rm -r {CURRENT_PATH}/{library['name']}.egg-info",
        }
    ]
}

update = {
    'purpose': f"Update {feature['name']}",
    'tasks': [
        {
            'purpose': f"Update {library['name']} library",
            'process_command': f"{library['install_command']} --force-reinstall",
            'requirements': [
                {
                    'purpose': 'Check Vixen environment installation',
                    'callback': lambda: os.path.isdir(VXENV_PATH),
                    'failure_details': 'Vixen Environment was not found'
                },
                {
                    'purpose': 'Check an existing library installation',
                    'callback': lambda: package_exist(library['name']),
                    'failure_details': f"{feature['name']} is not installed"
                }
            ]
        },
        {
            'purpose': 'Remove build folders',
            'process_command': f"sudo rm -r {CURRENT_PATH}/build && sudo rm -r {CURRENT_PATH}/{library['name']}.egg-info",
        }
    ]
}

remove = {
    'purpose': f"Remove {feature['name']}",
    'tasks': [
        {
            'purpose': f"Remove {library['name']} library",
            'process_command': library['remove_command'],
            'requirements': [
                {
                    'purpose': 'Check Vixen environment installation',
                    'callback': lambda: os.path.isdir(VXENV_PATH),
                    'failure_details': 'Vixen Environment was not found'
                },
                {
                    'purpose': 'Check an existing library installation',
                    'callback': lambda: package_exist(library['name']),
                    'failure_details': f"{feature['name']} is not installed"
                }
            ]
        }
    ]
}