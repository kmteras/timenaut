import os
import subprocess
import sys

if __name__ == '__main__':
    build_resources_command = [
        'pyside2-rcc',
        'res/resources.qrc',
        '-o', 'timewire/resources.py'
    ]

    subprocess.run(build_resources_command)

    command = [
        'pyinstaller',
        './main.py',
        '--name', 'timewire',
        '--icon', 'res/img/icon.ico',
        '--window',
        '-y',
    ]

    if sys.platform == 'linux':
        command += [
            '--hidden-import', 'timewire.core.linux',
        ]
    elif sys.platform == 'win32':
        command += [
            '--hidden-import', 'timewire.core.win32',
        ]

    subprocess.run(command)
