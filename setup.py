import sys

from cx_Freeze import setup, Executable

options = {"include_files": ["timewire/res"]}

base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Timewire",
    version="0.1",
    description="App for tracking time",
    options={"build_exe": options},
    executables=[Executable("timewire/main.py", base=base)]
)
