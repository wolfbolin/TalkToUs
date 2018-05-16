from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = 'C:\\ProgramZIP\\python-3.6.5\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\ProgramZIP\\python-3.6.5\\tcl\\tk8.6'

executables = [
   Executable('main.py', base=None, targetName='TalkToUs.exe', icon="favicon.ico")
]
build_exe_options = {'packages': ['flask', 'socket_module', 'jinja2', 'asyncio'], 'excludes': []}

setup(name='TalkToUs',
      version='0.1',
      description='Chat script',
      options={'build_exe': build_exe_options},
      executables=executables)
