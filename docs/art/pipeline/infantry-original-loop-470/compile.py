from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[4]
subprocess.run([sys.executable,str(R/'scripts/sprite-production.py'),str(Path(__file__).with_name('job.json')),'--mode','selected'],check=True)
