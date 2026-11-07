# 📦 PyGrassReal 4D Dynamic Splat (`.py4s`) File Format Specification
### Official Standard for 4D Gaussian Splatting (4DGS), Spatiotemporal Neural Deformation & Real-Time Deformable Physics

> **Copyright**: Copyright (c) 2026 **PyGrassReal AI** (https://pygrassreal.ai). All Rights Reserved.  
> **Brand / Originator**: **PyGrassReal**  
> **AI Engine**: **Kinnaree 1.0** — Video-to-4DGS Spatial Computing Engine  
> **Lineage**: **4D Dynamic Series (`.py4s`)** evolving from foundational `.py3s`  
> **Format Name**: PyGrassReal 4D Splat Single Container (`.py4s`)  
> **MIME Media Type**: `model/vnd.pygrassreal.py4s`  
> **Specification Version**: `1.0.0`  
> **Magic String**: `"PY4S"` (`0x50 0x59 0x34 0x53`)  
> **Endianness**: Little-Endian (LE)  
> **Header Size**: 128 Bytes  

---

## 🏛️ 1. Origin & Purpose

In the spatial computing and generative AI ecosystem:
1. **`.py3s` (S-Series):** Standard for **Static 3D Gaussian Splatting** combined with rigid physics collision (powered by Matchanu AI).
2. **`.py3m` (M-Series):** Standard for **3D Polygonal Mesh & PBR Textures** with manufacturing solid geometry (powered by Nilapat AI).
3. **`.py4s` (4D Dynamic Series):** The breakthrough evolution into the **temporal dimension ($t$)** through **4D Gaussian Splatting (4DGS)** — encapsulating photorealistic motion, fluid dynamics, character deformations, and synchronized real-time collision in a single, ultra-lightweight binary container (powered by **Kinnaree 1.0 AI**).

```text
                               🌟 PyGrassReal AI 🌟
                                         │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
   🔴 S-Series (.py3s)            🔵 M-Series (.py3m)             🟣 4D-Series (.py4s)
   Static 3DGS Container          Polygonal Mesh Container        4D Dynamic Splat Container
   • Engine: Matchanu 2.0         • Engine: Nilapat 2.5           • Engine: Kinnaree 1.0
   • Visual: Compressed 3DGS      • Visual: High-Detail PBR Mesh  • Visual: 4DGS (HexPlane + MLP)
   • Physics: 1:1 Static Hull     • Physics: 1:1 Solid Collision  • Physics: Real-Time Deformable Hitbox
   • MIME: ...pygrassreal.py3s    • MIME: ...pygrassreal.py3m     • MIME: ...pygrassreal.py4s
```

---

## 🔬 2. Scientific Foundations & Neural Architecture

The `.py4s` container integrates cutting-edge spatial computing research:
1. **Canonical 3D Gaussians:** A high-precision rest-pose point cloud at $t=0$, compressed using Adobe SPZ v4 algorithms for up to 85% compression while retaining 100% of Gaussians.
2. **HexPlane Spatiotemporal Deformation Field:** Projections of the 4D space $(x, y, z, t)$ into six orthogonal 2D feature planes:
   $$\text{HexPlane} = \{ R_{xy}, R_{xz}, R_{yz}, R_{xt}, R_{yt}, R_{zt} \}$$
   Multi-resolution feature vectors extracted from these planes are processed by a lightweight neural MLP to evaluate positional offsets ($\Delta \mu$), quaternion rotation perturbations ($\Delta q$), and scaling adjustments ($\Delta s$) for each Gaussian at timestamp $t$.
3. **Synchronized Deformable Collision:** A 3D spatial acceleration grid with K-Nearest Neighbors (KNN, $K=4$) and Inverse Distance Weighting (IDW) transferring Gaussian displacements to collision vertices in real-time ($<2\text{ms}$ execution per frame at 30/60 FPS).

---

## 📐 3. Binary Layout Overview

```text
┌────────────────────────────────────────────────────────┐
│             PY4S File Header (128 Bytes)               │  Offset 0x00
├────────────────────────────────────────────────────────┤
│ Section 1: Canonical 3DGS Layer (SPZ / PLY Base)       │  Offset = SpzOffset (normally 0x80)
├────────────────────────────────────────────────────────┤
│ Section 2: HexPlane Neural Deformation Layer           │  Offset = DeformationOffset
├────────────────────────────────────────────────────────┤
│ Section 3: Deformable Physics Collider Layer (GLB)     │  Offset = ColliderOffset
├────────────────────────────────────────────────────────┤
│ Section 4: Spatiotemporal Metadata Layer (JSON)        │  Offset = MetadataOffset
├────────────────────────────────────────────────────────┤
│ Section 5: Animated Preview Layer (WebP/MP4, Optional) │  Offset = ThumbnailOffset
└────────────────────────────────────────────────────────┘
```

---

## 📋 4. Fixed Binary Header (128 Bytes)

All multi-byte numeric values are stored in **Little-Endian (LE)** order:

| Offset (Hex) | Size (Bytes) | Data Type | Field Name | Description |
|---|---|---|---|---|
| `0x00` | 4 | `char[4]` | `Magic` | Must be `"PY4S"` (`0x50 0x59 0x34 0x53`) |
| `0x04` | 2 | `uint16` | `VersionMajor` | Major version number (currently `1`) |
| `0x06` | 2 | `uint16` | `VersionMinor` | Minor version number (currently `0`) |
| `0x08` | 4 | `uint32` | `SectionCount` | Number of active sections (typically `4` or `5`) |
| `0x0C` | 4 | `uint32` | `Flags` | Bitwise flags indicating encoding & compression |
| `0x10` | 8 | `uint64` | `SpzOffset` | Byte offset to Canonical 3DGS Base payload |
| `0x18` | 8 | `uint64` | `SpzSize` | Size in bytes of Canonical 3DGS Base payload |
| `0x20` | 8 | `uint64` | `DeformationOffset`| Byte offset to HexPlane Neural Deformation payload |
| `0x28` | 8 | `uint64` | `DeformationSize`  | Size in bytes of Deformation payload |
| `0x30` | 8 | `uint64` | `ColliderOffset`   | Byte offset to Deformable Physics Collider payload |
| `0x38` | 8 | `uint64` | `ColliderSize`     | Size in bytes of Collision geometry |
| `0x40` | 8 | `uint64` | `MetadataOffset`   | Byte offset to Spatiotemporal Metadata JSON |
| `0x48` | 8 | `uint64` | `MetadataSize`     | Size in bytes of Metadata JSON |
| `0x50` | 8 | `uint64` | `ThumbnailOffset`  | Byte offset to Animated Preview (0 if none) |
| `0x58` | 8 | `uint64` | `ThumbnailSize`    | Size in bytes of Animated Preview (0 if none) |
| `0x60` | 32 | `uint8[32]` | `Reserved`      | Reserved for future extensions (zero-filled) |

### Bit Flags (`Flags` 32-bit):
* `0x0001` - `PY4S_FLAG_SPZ_ZSTD`: Canonical base is compressed with Adobe SPZ / Zstandard.
* `0x0002` - `PY4S_FLAG_HEXPLANE_DEFORM`: Contains HexPlane neural deformation weights.
* `0x0004` - `PY4S_FLAG_COLLIDER_DEFORMABLE`: Collider mesh is rigged / mapped for real-time temporal deformation.
* `0x0010` - `PY4S_FLAG_HAS_ANIMATED_PREVIEW`: Container carries an animated preview payload.

---

## 💾 5. Section Specifications

### Section 1: Canonical 3DGS Base Layer
Contains the rest-pose ($t=0$) point cloud. Supported formats:
* **SPZ (`.spz`):** Quantized, Zstandard-compressed Gaussian splats retaining 100% of points.
* **PLY (`.ply`):** Standard binary Little-Endian 3DGS PLY.

### Section 2: HexPlane Neural Deformation Layer
Contains the temporal deformation model:
* **Format:** Binary tensor weights (`K4D1` signature) packing 6 planar feature grids ($XY, XZ, YZ, XT, YT, ZT$) and small MLP weights, or temporal keyframe trajectory offsets ($\Delta x, \Delta y, \Delta z, \Delta q$).

### Section 3: Deformable Physics Collider Layer
Contains low-poly collision geometry (GLB / OBJ) created by Nilapat collision engine. Vertex coordinates share the unscaled coordinate system of the canonical splats for instant 1:1 KNN-IDW vertex deformation.

### Section 4: Spatiotemporal Metadata Layer
A UTF-8 JSON document specifying temporal properties:
```json
{
  "format": "py4s",
  "version": "1.0.0",
  "generator": "Kinnaree 1.0 Video-to-4DGS",
  "temporal": {
    "total_frames": 90,
    "fps": 30,
    "duration_seconds": 3.0,
    "is_looping": true,
    "time_range": [0, 1]
  },
  "canonical_3dgs": {
    "gaussian_count": 65536,
    "format": "spz",
    "sh_degree": 0
  },
  "deformation": {
    "type": "trained_hexplane_keyframes",
    "encoding": "K4D1",
    "plane_resolution": [64, 64]
  },
  "asset": {
    "name": "cybernetic_warrior",
    "bounds": {
      "min": [-0.5, -0.8, -0.5],
      "max": [0.5, 0.8, 0.5]
    }
  }
}
```

### Section 5: Animated Preview Layer (Optional)
WebP, MP4, or GIF sequence for quick thumbnail preview in operating systems, content browsers, and web interfaces.

---

## 🔒 6. Intellectual Property & Conformance

* **Specification Standard:** PyGrassReal AI 4D Dynamic Specification.
* **Department of Intellectual Property (DIP) Thailand:** Recorded under Computer Program category.
* **International Protection:** Protected globally across 181 countries under the **Berne Convention**.
