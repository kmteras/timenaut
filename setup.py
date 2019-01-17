import subprocess
import os

if __name__ == '__main__':
    subprocess.run([
        'pyinstaller',
        'timewire/main.py',
        '--add-data', f'timewire/res/style{os.pathsep}res/style',
        '--name', 'timewire',
        '-y'
    ])
