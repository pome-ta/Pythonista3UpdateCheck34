from pathlib import Path
import webbrowser


def parent_level(level_int):
  return '../../' * level_int


origin_path = Path()

level = 2
target_url = origin_path / parent_level(level)

webbrowser.open(f'pythonista3://{target_url}')
