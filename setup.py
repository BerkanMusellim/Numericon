import cx_Freeze
import sys
import pandas
import numpy
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\oguz.sarigul\AppData\Local\Continuum\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\oguz.sarigul\AppData\Local\Continuum\Anaconda3\tcl\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("xzc.py", base=base)]

cx_Freeze.setup(
    name = "deneme",
    options = {"build_exe":{"packages":["tkinter", "pandas", "numpy"],
                            "include_files":["API Table 9.csv",
                                             r"C:\Users\oguz.sarigul\AppData\Local\Continuum\Anaconda3\DLLs\tcl86t.dll",
                                             r"C:\Users\oguz.sarigul\AppData\Local\Continuum\Anaconda3\DLLs\tk86t.dll"]}},
    version = "0.01",
    description = "This is the software where you can use when you need Table 9",
    executables = executables
)

