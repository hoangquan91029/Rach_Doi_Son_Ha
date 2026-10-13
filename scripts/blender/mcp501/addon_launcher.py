"""Root-authorized501 wrapper, isolated dependency path, pinned500 addon fork."""
from pathlib import Path
import hashlib
import runpy
import sys
repo=Path(__file__).resolve().parents[3]
venv=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/tools/mcp501/venv/lib/python3.14/site-packages')
if not venv.is_dir():raise ValueError('reviewed isolated Python3.14 dependency path absent')
sys.path.insert(0,str(venv))
source=repo/'scripts/blender/mcp500/offline_addon_candidate.py'
if hashlib.sha256(source.read_bytes()).hexdigest()!='219a496eda7248dfada013b5c83ce5e3356da590cbf24493dadb65ca92f03c7c':raise ValueError('reviewed addonfork source drift')
runpy.run_path(str(source),run_name='__main__')
