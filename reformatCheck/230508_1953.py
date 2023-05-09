import os
from pathlib import Path

style_path = os.path.expanduser('~/Documents/.style.yapf')
path = Path(style_path)

print(path.read_text())
