#!/usr/bin/env python3
# Copyright (c) 2026 PyGrassReal AI. All Rights Reserved.
# Brand: PyGrassReal (https://pygrassreal.ai)
# Specification: PyGrassReal 4D Splat Single Container Asset Format (.py4s)
"""
PyGrassReal 4D Dynamic Splat (.py4s) Generator Example
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
from py4s_codec import Py4sContainer, FLAG_SPZ_ZSTD, FLAG_HEXPLANE_DEFORM, FLAG_COLLIDER_DEFORMABLE


def main():
    print("=" * 60)
    print(" [*] PyGrassReal 4D Dynamic Splat (.py4s) Generator Example")
    print("=" * 60)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(output_dir, "sample_kinnaree.py4s")

    # 1. Canonical 3DGS Base Payload (SPZ compressed or PLY at t=0)
    canonical_base = b"SPZ_CANONICAL_3DGS_POINT_CLOUD_DATA_MOCK" * 40

    # 2. HexPlane Neural Deformation & Keyframes Payload (K4D1 binary)
    deformation_payload = b"K4D1_HEXPLANE_NEURAL_WEIGHTS_AND_KEYFRAMES_DATA" * 30

    # 3. Deformable Physics Collider Mesh Payload (GLB geometry)
    collider_mesh = b"GLTF_2_0_BINARY_DEFORMABLE_COLLIDER_MESH" * 20

    # 4. Spatiotemporal Metadata JSON
    metadata = {
        "format": "py4s",
        "version": "1.0.0",
        "generator": "Kinnaree 1.0 (4DGS Engine)",
        "asset": {
            "name": "sample_kinnaree",
            "gaussian_count": 50000,
            "bounds": {
                "min": [-0.5, -0.8, -0.5],
                "max": [0.5, 0.8, 0.5]
            }
        },
        "temporal": {
            "total_frames": 90,
            "fps": 30.0,
            "duration_seconds": 3.0,
            "is_looping": True,
            "time_range": [0.0, 1.0]
        },
        "canonical_3dgs": {
            "format": "spz",
            "gaussian_count": 50000,
            "sh_degree": 0
        },
        "deformation": {
            "type": "trained_hexplane_keyframes",
            "encoding": "K4D1",
            "plane_resolution": [64, 64]
        },
        "collider": {
            "format": "glb",
            "triangle_count": 12000,
            "vertex_count": 6000,
            "is_deformable": True
        }
    }

    print(f" [+] Assembling .py4s container for asset '{metadata['asset']['name']}'...")
    print(f"     - Temporal frames: {metadata['temporal']['total_frames']} at {metadata['temporal']['fps']} FPS ({metadata['temporal']['duration_seconds']}s)")
    print(f"     - Canonical 3DGS Base: {len(canonical_base):,} bytes")
    print(f"     - HexPlane Deformation: {len(deformation_payload):,} bytes")
    print(f"     - Deformable Collider: {len(collider_mesh):,} bytes")

    # Pack container
    packed_bytes = Py4sContainer.pack(
        spz_bytes=canonical_base,
        deformation_bytes=deformation_payload,
        collider_bytes=collider_mesh,
        metadata_dict=metadata
    )

    with open(sample_file, "wb") as f:
        f.write(packed_bytes)

    print(f" [SUCCESS] Written {len(packed_bytes):,} bytes to {sample_file}")

    # Verify unpack
    print(" [+] Verifying file readability by unpacking...")
    unpacked = Py4sContainer.unpack(packed_bytes)
    assert unpacked.metadata["format"] == "py4s"
    assert unpacked.metadata["temporal"]["total_frames"] == 90
    assert unpacked.spz_data == canonical_base
    assert unpacked.deformation_data == deformation_payload
    assert unpacked.collider_data == collider_mesh
    print(" [SUCCESS] Container verified: All 4 layers decoded accurately!")


if __name__ == "__main__":
    main()
