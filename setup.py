import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Adresseprinter",
    version = "0.4",
    description = "Adresseprinter",
    options = {"build_exe" : {"include_files" : ["data/template.html", "data/gui.ui", "data/icon.ico", "imageformats/qico4.dll"]}},
    executables = [Executable(script="MainWindow.py", icon="data/icon.ico", base=base)]
    )
