"""Week 1 environment check."""

from __future__ import annotations

import importlib
import sys


REQUIRED_PACKAGES = [
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("ipykernel", "jupyter kernel"),
]


def main() -> int:
    print("Python:", sys.version.split()[0])

    missing: list[str] = []
    for module_name, display_name in REQUIRED_PACKAGES:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            missing.append(display_name)
            print(f"[missing] {display_name}")
            continue

        version = getattr(module, "__version__", "installed")
        print(f"[ok] {display_name}: {version}")

    if missing:
        print()
        print("Some packages are missing.")
        print("Run: pip install -r requirements.txt")
        return 1

    print()
    print("Environment check passed.")
    print("Open notebooks/week01_baseline.ipynb in VS Code, Anaconda, or Jupyter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
