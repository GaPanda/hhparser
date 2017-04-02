from cx_Freeze import setup, Executable

setup(
    name = "hhparser",
    version = "0.1",
    description = "Program for parsing site https:\\hh.ru",
    executables = [Executable("main.py")],
    options = {"build_exe": {"packages": ["decimal", "uuid", "pyodbc", "lxml", "bs4"],
                             "include_files": ["config"]}},
)