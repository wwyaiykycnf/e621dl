from cx_Freeze import setup, Executable
import sys

sys.path.append('../')

from lib.version import VERSION

executables = [
    Executable('../e621dl.py')
]

setup(name='e621dl',
      version=VERSION,
      description='the automated e621dl.net downloader',
      data_files=[('.', ['Run_e621dl_In_Windows.bat'])],
      executables=executables,
      )
