# [Pythonista-Issues/sysinfo.py at master · omz/Pythonista-Issues](https://github.com/omz/Pythonista-Issues/blob/master/scripts/sysinfo.py)

import plistlib
import os
import sys
import platform
from objc_util import ObjCClass, on_main_thread
import clipboard


def get_pythonista_version_info():
  version = None
  bundle_version = None
  plist_path = os.path.abspath(os.path.join(sys.executable, '..',
                                            'Info.plist'))
  plist = plistlib.readPlist(plist_path)

  try:
    plist_path = os.path.abspath(
      os.path.join(sys.executable, '..', 'Info.plist'))
    plist = plistlib.readPlist(plist_path)

    version = plist['CFBundleShortVersionString']
    bundle_version = plist['CFBundleVersion']

  except Exception:
    print('Exception')
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
    '* {}, {}'.format(get_pythonista_version_info(),
                      get_python_interpreter_info()),
    '* {}'.format(get_device_info()),
  ])

  print('\n'.join([separator, info, separator]))
  print(
    'Please, attach everything between {} to your GitHub issue, many thanks.'.
    format(separator))
  clipboard.set(info)
  print(
    'System information was just stored in the system clipboard. You can paste it with Cmd V.'
  )


if __name__ == '__main__':
  main()

