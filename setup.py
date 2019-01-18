import subprocess
import os

if __name__ == '__main__':
    subprocess.run([
        'pyinstaller',
        './main.py',
        '--add-data', f'res/style{os.pathsep}res/style',
        '--name', 'timewire',
        '-y',
    ])
