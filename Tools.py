import platform
import os

class Tools:

    def is_linux():
        if Tools.detect_os() == 'linux':
            return True
        else:
            return False
        
    def is_windows():
        if Tools.detect_os() == 'windows':
            return True
        else:
            return False

    def detect_os():
        system = platform.system()
        if system == 'Linux':
            return 'linux'
        elif system == 'Windows':
            return 'windows'
        else:
            return 'unknown'

    def make_path_from_relative(relative_path):
        return os.path.join(os.path.dirname(__file__), relative_path)


