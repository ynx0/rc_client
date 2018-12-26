import sys
import os
from pathlib import Path

home = str(Path.home())
sys.path.insert(0, os.path.join(home, r'.virtualenvs\rc_client\Lib\site-packages\procbridge'))  # nasty setup which is very annoying
import procbridge
del sys.path[0], Path, home
