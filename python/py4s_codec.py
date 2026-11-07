#!/usr/bin/env python3
# Copyright (c) 2026 PyGrassReal AI. All Rights Reserved.
# Brand: PyGrassReal (https://pygrassreal.ai)
# Specification: PyGrassReal 4D Splat Single Container Asset Format (.py4s)
"""
PyGrassReal 4D Dynamic Splat (.py4s) Codec & CLI Tool
Official Reference Implementation by PyGrassReal AI (Kinnaree 1.0)
Packing and Unpacking tool for .py4s 4D Gaussian Splatting Assets.
"""

import sys
import os
import json
import struct
import argparse
from typing import Optional, Dict, Any, Tuple

HEADER_MAGIC = b"PY4S"
HEADER_FORMAT = "<4sHHIIQQQQQQQQQQ32s"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
assert HEADER_SIZE == 128, f"Header size must be 128 bytes, got {HEADER_SIZE}"

VERSION_MAJOR = 1
VERSION_MINOR = 0

FLAG_NONE = 0x0
FLAG_SPZ_ZSTD = 0x1
FLAG_HEXPLANE_DEFORM = 0x2
FLAG_COLLIDER_DEFORMABLE = 0x4
FLAG_TRAJECTORY_SPLINE = 0x8
FLAG_HAS_ANIMATED_PREVIEW = 0x10


class Py4sContainer:
    """
    Container class for .py4s 4D Gaussian Splatting file.
    Contains:
      - Canonical 3DGS Base (.spz / .ply)
      - Spatiotemporal HexPlane Neural Deformation Weights (.bin)
      - Deformable Physics Collider Mesh (.glb)
      - JSON Spatial & Temporal Metadata
      - Optional Animated Preview (WebP/MP4)
    """

    def __init__(self):
        self.version_major = VERSION_MAJOR
        self.version_minor = VERSION_MINOR
        self.flags = FLAG_SPZ_ZSTD | FLAG_HEXPLANE_DEFORM | FLAG_COLLIDER_DEFORMABLE
        self.spz_data: bytes = b""
        self.deformation_data: bytes = b""
        self.collider_data: bytes = b""
        self.metadata: Dict[str, Any] = {}
        self.thumbnail_data: bytes = b""

    @classmethod
    def pack(
        cls,
        spz_bytes: bytes,
        deformation_bytes: bytes,
        collider_bytes: bytes,
        metadata_dict: Dict[str, Any],
        thumbnail_bytes: bytes = b"",
    ) -> bytes:
        container = cls()
        container.spz_data = spz_bytes
        container.deformation_data = deformation_bytes
        container.collider_data = collider_bytes
        container.metadata = metadata_dict
        container.thumbnail_data = thumbnail_bytes

        meta_json = json.dumps(metadata_dict, ensure_ascii=False, indent=2).encode("utf-8")

        current_offset = HEADER_SIZE

        # Section 1: Canonical 3DGS Base
        spz_offset = current_offset
        spz_size = len(container.spz_data)
        current_offset += spz_size

        # Section 2: HexPlane Neural Deformation
        deform_offset = current_offset
        deform_size = len(container.deformation_data)
        current_offset += deform_size

        # Section 3: Deformable Physics Collider
        collider_offset = current_offset
        collider_size = len(container.collider_data)
        current_offset += collider_size

        # Section 4: Metadata JSON
        meta_offset = current_offset
        meta_size = len(meta_json)
        current_offset += meta_size

        # Section 5: Animated Preview
        section_count = 4
        thumb_offset = 0
        thumb_size = 0
        flags = FLAG_SPZ_ZSTD | FLAG_HEXPLANE_DEFORM | FLAG_COLLIDER_DEFORMABLE

        if container.thumbnail_data:
            thumb_offset = current_offset
            thumb_size = len(container.thumbnail_data)
            current_offset += thumb_size
            section_count = 5
            flags |= FLAG_HAS_ANIMATED_PREVIEW

        header = struct.pack(
            HEADER_FORMAT,
            HEADER_MAGIC,
            container.version_major,
            container.version_minor,
            section_count,
            flags,
            spz_offset,
            spz_size,
            deform_offset,
            deform_size,
            collider_offset,
            collider_size,
            meta_offset,
            meta_size,
            thumb_offset,
            thumb_size,
            b"\x00" * 32,
        )

        return (
            header
            + container.spz_data
            + container.deformation_data
            + container.collider_data
            + meta_json
            + container.thumbnail_data
        )

    @classmethod
    def unpack(cls, py4s_bytes: bytes) -> "Py4sContainer":
        if len(py4s_bytes) < HEADER_SIZE:
            raise ValueError(f"Invalid file: size {len(py4s_bytes)} is smaller than header {HEADER_SIZE} bytes")

        (
            magic,
            v_major,
            v_minor,
            sec_count,
            flags,
            spz_off,
            spz_sz,
            deform_off,
            deform_sz,
            col_off,
            col_sz,
            meta_off,
            meta_sz,
            thumb_off,
            thumb_sz,
            reserved,
        ) = struct.unpack(HEADER_FORMAT, py4s_bytes[:HEADER_SIZE])

        if magic != HEADER_MAGIC:
            raise ValueError(f"Invalid magic: expected {HEADER_MAGIC.decode()}, got {magic!r}")

        container = cls()
        container.version_major = v_major
        container.version_minor = v_minor
        container.flags = flags

        if spz_sz > 0:
            container.spz_data = py4s_bytes[spz_off : spz_off + spz_sz]

        if deform_sz > 0:
            container.deformation_data = py4s_bytes[deform_off : deform_off + deform_sz]

        if col_sz > 0:
            container.collider_data = py4s_bytes[col_off : col_off + col_sz]

        if meta_sz > 0:
            raw_meta = py4s_bytes[meta_off : meta_off + meta_sz].decode("utf-8")
            container.metadata = json.loads(raw_meta)

        if thumb_sz > 0:
            container.thumbnail_data = py4s_bytes[thumb_off : thumb_off + thumb_sz]

        return container


def cmd_pack(args):
    with open(args.spz, "rb") as f:
        spz_data = f.read()

    deform_data = b""
    if args.deformation and os.path.isfile(args.deformation):
        with open(args.deformation, "rb") as f:
            deform_data = f.read()

    collider_data = b""
    if args.collider and os.path.isfile(args.collider):
        with open(args.collider, "rb") as f:
            collider_data = f.read()

    meta_dict = {}
    if args.metadata and os.path.isfile(args.metadata):
        with open(args.metadata, "r", encoding="utf-8") as f:
            meta_dict = json.load(f)
    else:
        meta_dict = {
            "format": "py4s",
            "version": f"{VERSION_MAJOR}.{VERSION_MINOR}.0",
            "generator": "Kinnaree 1.0 (4DGS)",
            "temporal": {"duration_seconds": 3.0, "fps": 30, "is_looping": True},
        }

    thumb_data = b""
    if args.thumbnail and os.path.isfile(args.thumbnail):
        with open(args.thumbnail, "rb") as f:
            thumb_data = f.read()

    packed = Py4sContainer.pack(spz_data, deform_data, collider_data, meta_dict, thumb_data)
    with open(args.output, "wb") as f:
        f.write(packed)

    print(f"[+] Successfully packed {len(packed):,} bytes -> {args.output}")


def cmd_unpack(args):
    with open(args.input, "rb") as f:
        data = f.read()

    container = Py4sContainer.unpack(data)
    out_dir = args.out_dir or "."
    os.makedirs(out_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(args.input))[0]

    spz_file = os.path.join(out_dir, f"{base_name}_canonical.spz")
    with open(spz_file, "wb") as f:
        f.write(container.spz_data)

    if container.deformation_data:
        deform_file = os.path.join(out_dir, f"{base_name}_hexplane.bin")
        with open(deform_file, "wb") as f:
            f.write(container.deformation_data)

    if container.collider_data:
        col_file = os.path.join(out_dir, f"{base_name}_collider.glb")
        with open(col_file, "wb") as f:
            f.write(container.collider_data)

    meta_file = os.path.join(out_dir, f"{base_name}_meta.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(container.metadata, f, indent=2, ensure_ascii=False)

    if container.thumbnail_data:
        thumb_ext = "webp" if container.thumbnail_data[:4] == b"RIFF" else "mp4"
        thumb_file = os.path.join(out_dir, f"{base_name}_preview.{thumb_ext}")
        with open(thumb_file, "wb") as f:
            f.write(container.thumbnail_data)

    print(f"[+] Unpacked {args.input} successfully to {out_dir}/")


def cmd_info(args):
    with open(args.input, "rb") as f:
        data = f.read()

    container = Py4sContainer.unpack(data)
    print("=" * 60)
    print(f"📦 PyGrassReal 4D Splat (.py4s) Asset Inspection")
    print(f"Format Version: {container.version_major}.{container.version_minor}")
    print(f"Bit Flags: {hex(container.flags)}")
    print(f"Canonical 3DGS Base: {len(container.spz_data):,} bytes")
    print(f"HexPlane Deformation Field: {len(container.deformation_data):,} bytes")
    print(f"Deformable Collider: {len(container.collider_data):,} bytes")
    print(f"Animated Preview: {len(container.thumbnail_data):,} bytes")
    print("-" * 60)
    print(f"Metadata:")
    print(json.dumps(container.metadata, indent=2, ensure_ascii=False))
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="PyGrassReal 4D Splat (.py4s) Codec CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # pack
    p_pack = subparsers.add_parser("pack", help="Pack assets into .py4s container")
    p_pack.add_argument("--spz", required=True, help="Canonical 3DGS Base (.spz or .ply)")
    p_pack.add_argument("--deformation", help="HexPlane deformation weights (.bin)")
    p_pack.add_argument("--collider", help="Deformable collision mesh (.glb)")
    p_pack.add_argument("--metadata", help="Metadata JSON file")
    p_pack.add_argument("--thumbnail", help="Preview animated image/video")
    p_pack.add_argument("-o", "--output", required=True, help="Output .py4s file path")
    p_pack.set_defaults(func=cmd_pack)

    # unpack
    p_unpack = subparsers.add_parser("unpack", help="Unpack .py4s container into components")
    p_unpack.add_argument("-i", "--input", required=True, help="Path to .py4s file")
    p_unpack.add_argument("-o", "--out-dir", help="Output directory")
    p_unpack.set_defaults(func=cmd_unpack)

    # info
    p_info = subparsers.add_parser("info", help="Display metadata and section statistics")
    p_info.add_argument("-i", "--input", required=True, help="Path to .py4s file")
    p_info.set_defaults(func=cmd_info)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

