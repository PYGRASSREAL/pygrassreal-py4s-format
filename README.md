<div align="center">

<a href="https://pygrassreal.ai">
  <img src="https://raw.githubusercontent.com/PYGRASSREAL/pygrassreal-py4s-format/main/assets/logo.png" alt="PyGrassReal Logo" width="220" />
</a>

# PyGrassReal 4D Dynamic Splat (`.py4s`) File Format
### The Generational 4D Spatiotemporal Asset Standard of the PyGrassReal Ecosystem

[![Specification](https://img.shields.io/badge/Specification-v1.0.0-blue.svg)](SPECIFICATION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NVIDIA Inception](https://img.shields.io/badge/NVIDIA%20Inception-Program%20Member-76B900?logo=nvidia&logoColor=white)](https://www.nvidia.com/en-us/startups/)
[![Copyright DIP](https://img.shields.io/badge/Copyright%20DIP-Thailand%20Recorded-success.svg)](docs/COPYRIGHT_RECORDATION_GUIDE.md)
[![MIME Type](https://img.shields.io/badge/MIME-model%2Fvnd.pygrassreal.py4s-blue.svg)](docs/IANA_MIME_REGISTRATION_DRAFT.md)
[![Magic String](https://img.shields.io/badge/Magic-PY4S-purple.svg)](#binary-layout)
[![Engines](https://img.shields.io/badge/Engines-Unreal%205%20%7C%20Unity%20%7C%20Three.js%20%7C%20Python-purple.svg)](#implementations)
[![Lineage](https://img.shields.io/badge/Lineage-PyGrassReal%204D%20Dynamic-violet.svg)](#-evolutionary-lineage-from-py3s-to-py4s)

**The Official Single-Container Asset Standard Uniting 4D Dynamic Gaussian Splatting, HexPlane Neural Deformation, and Real-Time Deformable Physics Collision.**

[📖 Read Specification](SPECIFICATION.md) • [📋 DIP Copyright Guide](docs/COPYRIGHT_RECORDATION_GUIDE.md) • [🐍 Python SDK](python/) • [⚡ C++ Implementation](cpp/) • [🌐 TypeScript / Web](typescript/) • [🏛️ Official Platform](https://pygrassreal.ai)

<br/>

<a href="https://www.nvidia.com/en-us/startups/">
  <img src="assets/nvidia-inception-program-badge-rgb-for-screen.svg" alt="NVIDIA Inception Program Member" width="340" style="background: #ffffff; border-radius: 8px; padding: 10px 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);" />
</a>

<p><strong>PyGrassReal is a member of the NVIDIA Inception program</strong>, nurturing cutting-edge startups revolutionizing spatial computing, neural rendering, and generative 4D technologies.</p>

</div>

---

## 🏛️ Evolutionary Lineage: From `.py3s` to `.py4s`

The `.py4s` format represents the second major milestone in the **PyGrassReal Spatial Computing Lineage**:
- **`.py3s` (Foundational 3DGS Root):** Standardized by Matchanu AI for static 3D Gaussian Splats with 1:1 rigid physics collision.
- **`.py4s` (Generational 4DGS Leap):** Standardized by **Kinnaree 1.0 AI**, expanding the spatial coordinate system into the **temporal dimension ($t$)**. It packages the canonical 3D base, neural HexPlane spatiotemporal deformation fields, and real-time deforming physics hitboxes into a single, compact binary container.

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

## 💡 The 4D Spatial Computing Challenge

Traditional 4D Gaussian Splatting and dynamic neural representations suffer from severe deployment friction:
1. **File Fragmentation:** Storing separate keyframe PLY files per frame consumes gigabytes of storage (e.g. 90 frames $\times$ 15MB = 1.35 GB for a 3-second clip).
2. **Ghost Dynamics:** Traditional 4DGS is purely optical radiance with **zero physics collision**, causing game actors and cameras to pass straight through moving characters.
3. **Desynchronized Physics:** Manually rigging collision cages to neural Gaussian deformation leads to desynchronized scaling, jitter, and manual alignment overhead.

---

## 🚀 The PyGrassReal Solution: Native 4D Single-Container Standard

The **`.py4s`** format solves this industry bottleneck by packaging everything needed for photorealistic dynamic rendering and real-time interactive physics in one file:

1. **Canonical 3DGS Base (Adobe SPZ Compressed):** Quantized and compressed at the rest pose ($t=0$), reducing file size by up to **85%** while retaining 100% of Gaussians without pruning.
2. **HexPlane Neural Deformation Layer:** Continuous spatiotemporal deformation field projecting 4D coordinates $(x,y,z,t)$ across 6 orthogonal feature planes ($XY, XZ, YZ, XT, YT, ZT$) with lightweight MLP offsets for positions ($\Delta \mu$), rotations ($\Delta q$), and scales ($\Delta s$).
3. **Real-Time Synchronized Deformable Collider:** Low-poly collision mesh deformed per frame at 30/60 FPS via a 3D spatial hash grid with K-Nearest Neighbors (KNN, $K=4$) and Inverse Distance Weighting (IDW).
4. **Spatiotemporal Metadata:** Comprehensive temporal parameters including duration, frame rate, looping rules, and coordinate bounds.
5. **Animated Preview:** Optional embedded motion preview for instant OS and web gallery previews.

---

## 📐 Binary Layout Overview

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

## ⚡ Quick Start

### 🐍 Python SDK
```python
from py4s_codec import Py4sCodec, Py4sContainer

# Unpack a .py4s file
container = Py4sCodec.unpack_file("kinnaree_warrior.py4s")
print(f"Total Frames: {container.metadata['temporal']['total_frames']}")
print(f"FPS: {container.metadata['temporal']['fps']}")
print(f"Canonical 3DGS Size: {len(container.spz_data):,} bytes")

# Pack a new .py4s container
packed_bytes = Py4sCodec.pack(container)
with open("output.py4s", "wb") as f:
    f.write(packed_bytes)
```

### 🌐 TypeScript / Web SDK
```typescript
import { Py4sCodec, isPy4sBuffer, getPy4sBaseVisual } from './py4sCodec';

const response = await fetch('model.py4s');
const arrayBuffer = await response.arrayBuffer();

if (isPy4sBuffer(arrayBuffer)) {
  const container = Py4sCodec.unpack(arrayBuffer);
  console.log('4DGS Metadata:', container.metadata);
  const visual = getPy4sBaseVisual(arrayBuffer);
  console.log(`Base Visual Format: ${visual.format}`);
}
```

### ⚡ C++ / Unreal Engine 5
```cpp
#include "Py4sReader.h"

PyGrassReal::FPy4sContainer Container;
if (PyGrassReal::FPy4sReader::ReadFromFile(TEXT("D:/Models/kinnaree.py4s"), Container))
{
    UE_LOG(LogTemp, Log, TEXT("Loaded 4DGS: %d frames at %f FPS"), 
        Container.Metadata.TotalFrames, Container.Metadata.FPS);
}
```

---

## 📊 Benchmark & File Size Comparison

| Asset Type | Raw 4DGS PLY Frames (90 frames) | Uncompressed `.py4s` (Raw PLY) | `.py4s` with Adobe SPZ v4 | Size Reduction |
|:---|:---:|:---:|:---:|:---:|
| **Cybernetic Character** | 1,080 MB | 11.87 MB | **2.24 MB** | **-99.8% vs raw frames / -81% vs container** |
| **Robotic Arm 3D Printing**| 1,260 MB | 14.12 MB | **2.68 MB** | **-99.8% vs raw frames / -81% vs container** |

---

## 📜 Intellectual Property & Copyright Recordation

* **DIP Thailand Registration:** Recorded with the Department of Intellectual Property (DIP), Thailand, under the Computer Program category. See [docs/COPYRIGHT_RECORDATION_GUIDE.md](docs/COPYRIGHT_RECORDATION_GUIDE.md) for full application templates.
* **International Protection:** Protected automatically across 181 countries under the **Berne Convention**.
* **License:** Permissive open-source [MIT License](LICENSE).
