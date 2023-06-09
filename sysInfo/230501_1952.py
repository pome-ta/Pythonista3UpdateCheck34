import plistlib
import os
import sys
import platform
from pathlib import Path
from objc_util import ObjCClass, on_main_thread
import clipboard


def get_pythonista_version_info():
  version = None
  bundle_version = None

  try:
    plist_path = os.path.abspath(
      os.path.join(sys.executable, '..', 'Info.plist'))
    plist_data = Path(plist_path).read_bytes()
    plist = plistlib.loads(plist_data)

    version = plist['CFBundleShortVersionString']
    bundle_version = plist['CFBundleVersion']

  except Exception:
    pass

  return 'Pythonista {} ({})'.format(version or 'N/A', bundle_version or 'N/A')


def get_python_interpreter_info():
  return 'Default interpreter {}.{}.{}'.format(*sys.version_info)


def get_device_info():
  device = ObjCClass('UIDevice').currentDevice()
  main_screen = ObjCClass('UIScreen').mainScreen()
  native_size = main_screen.nativeBounds().size

  return 'iOS {}, model {}, resolution (portrait) {} x {} @ {}'.format(
    device.systemVersion(), platform.machine(), native_size.width,
    native_size.height, main_screen.nativeScale())


@on_main_thread  # clipboard.set or freeze
def main():
  separator = '--- SYSTEM INFORMATION ---'

  info = '\n'.join([
    '**System Information**',
    '',
    f'* {get_pythonista_version_info()}, {get_python_interpreter_info()}',
    f'* {get_device_info()}',
  ])

  print('\n'.join([separator, info, separator]))
  print(
    f'Please, attach everything between {separator} to your GitHub issue, many thanks.'
  )
  clipboard.set(info)
  print(
    'System information was just stored in the system clipboard. You can paste it with Cmd V.'
  )


if __name__ == '__main__':
  main()

