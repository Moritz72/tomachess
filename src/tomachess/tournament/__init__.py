import pkgutil
import importlib
import sys

package = sys.modules[__name__]

for loader, name, is_pkg in pkgutil.iter_modules(package.__path__):
    if is_pkg:
        importlib.import_module(f"{__name__}.{name}")
