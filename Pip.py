import platform
import os
from pathlib import Path
import subprocess
import adsk.core, traceback  # pylint: disable=import-error
import sys
def install_package(package_name):
    print(f"Installing {package_name}...")
    try:
        python_path = str(Path(os.__file__).parents[1] / 'python.exe')
    except:
        python_path = sys.executable
    try:
        import pip
    except ImportError:
        get_pip_filepath = os.path.join(os.path.dirname(__file__), 'get-pip.py')
        subprocess.check_call([python_path, get_pip_filepath])

    try:
        subprocess.check_call([python_path, '-m', 'pip', 'install', package_name])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")
        raise

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        lib_url, cancelled = ui.inputBox('Enter the name of the Python library to import in Fusion 360', 'PipToFusion360')
        if cancelled:
            ui.messageBox('Process aborted', 'PipToFusion360', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
            return

        install_package(lib_url)

        if ui:
            ui.messageBox('Install successful')
    except adsk.AbortError:
        pass  # User aborted, do nothing
    except Exception as ex:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

