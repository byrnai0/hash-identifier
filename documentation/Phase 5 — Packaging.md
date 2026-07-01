___

Phase 5 packaged the entire HashPilot project into a standalone
`hashpilot.exe` using PyInstaller. The exe runs on any Windows machine
from CMD with zero Python installation required. All five source files,
the Rich library, and Python itself are bundled into a single binary.

___

## Tool Used: PyInstaller

PyInstaller works by tracing all imports in your entry point (`cli.py`),
collecting every dependency (including Rich, and all my `.py` files),
and packing them into a self-extracting executable. When the exe runs,
it unpacks to a temp folder, boots a bundled Python interpreter, and
runs the code — all invisibly.

Install:
```bash
pip install pyinstaller
```

___

## Antivirus False Positives

Windows Defender sometimes flags PyInstaller exes as suspicious. This
is a known false positive — PyInstaller bundles Python in a way that
resembles packer tools used by malware. Fix: add the `dist/` folder
as a Windows Defender exclusion, or right-click → Properties → Unblock.

___

## Final File Structure

```
hashpilot/
├── hash_db.py
├── scorer.py
├── hints.py
├── matcher.py
├── cli.py
└── dist/
└── hashpilot.exe ← final deliverable
```

