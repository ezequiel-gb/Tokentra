"""Copy installed dependency licence notices into the distribution sources."""
from importlib.metadata import distribution
from pathlib import Path
import shutil
import sys

destination = Path(__file__).resolve().parents[1] / "packaging/third-party"
destination.mkdir(parents=True, exist_ok=True)
python_licence = Path(sys.base_prefix) / "LICENSE.txt"
if python_licence.exists():
    shutil.copyfile(python_licence, destination / "Python-LICENSE.txt")
for name in ("PySide6_Essentials", "shiboken6", "tiktoken", "regex", "requests", "urllib3",
             "certifi", "charset_normalizer", "idna", "pyinstaller"):
    package = distribution(name)
    found = []
    for file in package.files or []:
        if any(part.upper().startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE")) for part in file.parts):
            source = Path(package.locate_file(file))
            if source.is_file():
                target = destination / name / str(file).replace("/", "_").replace("\\", "_")
                target.parent.mkdir(exist_ok=True)
                shutil.copyfile(source, target)
                found.append(target.name)
    print(name, package.version, len(found), "licence files")
