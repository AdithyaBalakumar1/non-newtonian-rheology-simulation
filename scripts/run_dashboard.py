#!/usr/bin/env python3
"""Launch the upgraded Dash dashboard."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard import app

if __name__ == "__main__":
    app.run(debug=True)
