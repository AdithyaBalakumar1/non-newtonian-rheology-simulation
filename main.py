"""Thin wrapper for backward compatibility. Calls scripts/run_rheology.py."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.run_rheology import main

if __name__ == "__main__":
    main()
