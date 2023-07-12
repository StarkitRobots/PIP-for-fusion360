# Author-Jerome Briot
# Contact-jbtechlab@gmail.com
# Description-Install scripts or add-ins from GitHub

import adsk
import adsk.core
import adsk.fusion
import traceback

import sys
import os
packagepath = os.path.join(os.path.dirname(sys.argv[0]), 'Lib/site-packages/')
if packagepath not in sys.path:
    sys.path.append(packagepath)


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    (pip_name, cancelled) = ui.inputBox(
        'Enter the PIP library to import in Fusion 360', 'Install')
    try:
        def install_and_import(package):
            import importlib
            try:
                importlib.import_module(package)
            except ImportError:
                import pip
                pip.main(['install', package])
            finally:
                globals()[package] = importlib.import_module(package)
        app = adsk.core.Application.get()
        ui = app.userInterface
        install_and_import(pip_name)
        ui.messageBox(pip_name, pip_name)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
   