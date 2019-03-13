import os
import subprocess
import sys

if __name__ == '__main__':
    command = [
        'pyinstaller',
        './main.py',
        '--add-data', f'res/style{os.pathsep}res/style',
        '--add-data', f'res/img{os.pathsep}res/img',
        '--add-data', f'res/qml{os.pathsep}res/qml',
        '--name', 'timewire',
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
