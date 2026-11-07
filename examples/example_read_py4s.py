#!/usr/bin/env python3
# Copyright (c) 2026 PyGrassReal AI. All Rights Reserved.
# Brand: PyGrassReal (https://pygrassreal.ai)
# Specification: PyGrassReal 4D Splat Single Container Asset Format (.py4s)
"""
PyGrassReal 4D Dynamic Splat (.py4s) Reader & Inspection Example
Official Reference Implementation by PyGrassReal AI (Kinnaree 1.0)
"""

import io
import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))
from py4s_codec import Py4sContainer


def main():
    if len(sys.argv) < 2:
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_kinnaree.py4s")
        if not os.path.isfile(sample_path):
            print("Usage: python example_read_py4s.py <file.py4s>")
            sys.exit(1)
        target = sample_path
    else:
        target = sys.argv[1]

    print("=" * 60)
    print(f" [*] Inspecting PyGrassReal 4D Splat: {os.path.basename(target)}")
    print("=" * 60)

    with open(target, "rb") as f:
        file_bytes = f.read()

    container = Py4sContainer.unpack(file_bytes)
    meta = container.metadata

    print(f" Container Size: {len(file_bytes):,} bytes")
    print(f" Format: {meta.get('format')} v{meta.get('version')}")
    print(f" Generator: {meta.get('generator', 'Unknown')}")
    
    temporal = meta.get("temporal", {})
    print(f"\n [1] Temporal Configuration:")
    print(f"     Total Frames: {temporal.get('total_frames', 'N/A')}")
    print(f"     FPS: {temporal.get('fps', 'N/A')}")
    print(f"     Duration: {temporal.get('duration_seconds', 'N/A')} seconds")
    print(f"     Looping: {temporal.get('is_looping', False)}")

    print(f"\n [2] Internal Layers:")
    print(f"     Canonical 3DGS Base: {len(container.spz_data):,} bytes")
    print(f"     HexPlane Deformation: {len(container.deformation_data):,} bytes")
    print(f"     Deformable Collider: {len(container.collider_data):,} bytes")
    print(f"     Thumbnail Preview: {len(container.thumbnail_data):,} bytes")

    print("\n [SUCCESS] .py4s file read and validated successfully!")


if __name__ == "__main__":
    main()
