import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "hhparser",
    version = "1.3",
    description = "Program for parsing site https:\\hh.ru",
    executables = [Executable("hhparser_cmd.py"), Executable("hhparser_ui.pyw", base = base)],
    options = {"build_exe": {"packages": ["decimal", "uuid", "pyodbc", "lxml", "bs4", "configparser"],
                             "include_files": ["config.ini", "mssql", "text.txt"]}},
)