<div align="center">

<a href="https://pygrassreal.ai">
  <img src="https://raw.githubusercontent.com/PYGRASSREAL/pygrassreal-py4s-format/main/assets/logo.png" alt="PyGrassReal Logo" width="220" />
</a>

# PyGrassReal 4D Dynamic Splat (`.py4s`) File Format
### The Generational 4D Spatiotemporal Asset Standard for Unreal Engine 5, Unity, and Real-Time Graphics

[![Specification](https://img.shields.io/badge/Specification-v1.0.0-blue.svg)](SPECIFICATION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NVIDIA Inception](https://img.shields.io/badge/NVIDIA%20Inception-Program%20Member-76B900?logo=nvidia&logoColor=white)](https://www.nvidia.com/en-us/startups/)
[![Copyright DIP](https://img.shields.io/badge/Copyright%20DIP-Thailand%20Recorded-success.svg)](docs/COPYRIGHT_RECORDATION_GUIDE.md)
[![MIME Type](https://img.shields.io/badge/MIME-model%2Fvnd.pygrassreal.py4s-blue.svg)](docs/IANA_MIME_REGISTRATION_DRAFT.md)
[![Magic String](https://img.shields.io/badge/Magic-PY4S-purple.svg)](#binary-layout-specification)
[![Engines](https://img.shields.io/badge/Engines-Unreal%205%20%7C%20Unity%20%7C%20Three.js%20%7C%20Python-purple.svg)](#-how-to-use-py4s-in-game-engines)

**The Official Single-Container Asset Standard Uniting 4D Dynamic Gaussian Splatting, HexPlane Neural Deformation, and Real-Time Deformable Physics Collision.**

[📖 Read Specification](SPECIFICATION.md) • [📋 DIP Copyright Guide](docs/COPYRIGHT_RECORDATION_GUIDE.md) • [🎮 Unreal Engine 5](cpp/) • [🎯 Unity C#](unity/) • [🐍 Python SDK](python/) • [🌐 TypeScript / Web](typescript/) • [🏛️ Official Platform](https://pygrassreal.ai)

<br/>

<a href="https://www.nvidia.com/en-us/startups/">
  <img src="assets/nvidia-inception-program-badge-rgb-for-screen.svg" alt="NVIDIA Inception Program Member" width="340" style="background: #ffffff; border-radius: 8px; padding: 10px 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);" />
</a>

<p><strong>PyGrassReal is a member of the NVIDIA Inception program</strong>, nurturing cutting-edge startups revolutionizing spatial computing, neural rendering, and generative 4D technologies.</p>

</div>

---

## 💡 What is `.py4s` and How Does It Work?

Traditional 4D Gaussian Splatting and dynamic neural representations suffer from critical bottlenecks in production game engines:
1. **Extreme File Fragmentation:** Storing dynamic splats as separate keyframe `.ply` files per frame requires gigabytes of disk storage (e.g., 90 frames $\times$ 15 MB = **1.35 GB** for a 3-second clip).
2. **Zero Physical Interaction:** Traditional 4DGS is purely optical radiance with **no physical hitbox**, causing characters and cameras in Unreal Engine 5 and Unity to pass straight through animated subjects.
3. **Desynchronized Physics:** Manually rigging collision cages to neural Gaussian deformation leads to desynchronized scaling, jitter, and manual alignment overhead.

### The `.py4s` Solution: Unified Single-Container 4D Dynamic Asset

The **`.py4s`** format solves this by bundling **Canonical 3DGS Base**, **Neural Spatiotemporal Deformation (HexPlane)**, and **Synchronized Deformable Collision** into a single binary file:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      Kinnaree 1.0 AI (Video to 4DGS)                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  PyGrassReal .py4s Unified Container                   │
│                                                                        │
│  ┌───────────────────────┐  ┌───────────────────────────────────────┐  │
│  │  Canonical 3DGS Base  │  │   HexPlane Neural Deformation Field   │  │
│  │  (Adobe SPZ Quantized)│  │   (6 Planes XY/XZ/YZ/XT/YT/ZT + MLP)  │  │
│  └───────────┬───────────┘  └───────────────────┬───────────────────┘  │
│              │                                  │                      │
│              └─────────────────┬────────────────┘                      │
│                                ▼                                       │
│             ┌──────────────────────────────────────┐                   │
│             │ Dynamic Gaussians at Timestamp (t):  │                   │
│             │ Position: μ(t) = μ₀ + Δμ(t)          │                   │
│             │ Rotation: q(t) = q₀ ⊗ Δq(t)          │                   │
│             │ Scale:    s(t) = s₀ · exp(Δs(t))     │                   │
│             └──────────────────┬───────────────────┘                   │
│                                │ (Synchronized KNN IDW)                │
│                                ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Real-Time Deformable Physics Collider (GLB Hitbox deformed at t) │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Spatiotemporal Metadata (JSON: FPS, Duration, Bounds, Looping)   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
🎮 Unreal Engine 5 (UE5)                                        🎯 Unity Engine (URP / HDRP)
• Native C++ FPy4sReader                                        • Native C# Py4sReader
• GPU Compute / Niagara Dynamic Splats                          • Compute Shader Per-Frame Deformation
• Chaos Deformable Hitbox Collision                             • PhysX Deformable MeshCollider
```

---

## 🔬 Core Components Inside a `.py4s` Container

| Section | Component | Description & Functionality |
|:---|:---|:---|
| **Section 1** | **Canonical 3DGS Base** | Quantized 3D Gaussian rest-pose ($t=0$). Compressed using Adobe SPZ v4 algorithms, shrinking raw PLY by up to **85%** while retaining 100% of Gaussians without pruning. |
| **Section 2** | **HexPlane Neural Deformation** | Continuous spatiotemporal neural field. Projects $(x, y, z, t)$ across 6 orthogonal 2D planes ($R_{xy}, R_{xz}, R_{yz}, R_{xt}, R_{yt}, R_{zt}$) with a lightweight MLP predicting per-Gaussian offsets ($\Delta \mu, \Delta q, \Delta s$). |
| **Section 3** | **Synchronized Deformable Collider** | Precision low-poly collision geometry (GLB). Dynamically deformed per frame at 30/60 FPS via a 3D spatial hash grid with K-Nearest Neighbors ($K=4$) and Inverse Distance Weighting (IDW). |
| **Section 4** | **Spatiotemporal Metadata** | JSON structure specifying frame rate, duration, looping configuration, bounding boxes, and coordinate space parameters. |
| **Section 5** | **Animated Preview** | Optional embedded motion preview (WebP / MP4) for instant zero-load gallery previews. |

---

## 📐 Binary Layout Specification

A `.py4s` file consists of a fixed **128-byte Header** followed by 5 contiguous payload sections:

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

### Header Structure (128 Bytes)
* `0x00..0x03` (4B): Magic Bytes `"PY4S"` (`0x50 0x59 0x34 0x53`)
* `0x04..0x05` (2B): Version Major (Default: `1`)
* `0x06..0x07` (2B): Version Minor (Default: `0`)
* `0x08..0x0B` (4B): Section Count (`4` or `5`)
* `0x0C..0x0F` (4B): Flags (`0x1` SPZ Zstd, `0x2` HexPlane, `0x4` Deformable Collider, `0x10` Preview)
* `0x10..0x17` (8B): Section 1 Offset (Canonical 3DGS)
* `0x18..0x1F` (8B): Section 1 Byte Length
* `0x20..0x27` (8B): Section 2 Offset (HexPlane Deformation)
* `0x28..0x2F` (8B): Section 2 Byte Length
* `0x30..0x37` (8B): Section 3 Offset (Deformable Collider)
* `0x38..0x3F` (8B): Section 3 Byte Length
* `0x40..0x47` (8B): Section 4 Offset (Metadata JSON)
* `0x48..0x4F` (8B): Section 4 Byte Length
* `0x50..0x57` (8B): Section 5 Offset (Animated Preview)
* `0x58..0x5F` (8B): Section 5 Byte Length
* `0x60..0x7F` (32B): Reserved / Future Expansions

---

## 🎮 How to Use `.py4s` in Game Engines

### 1. ⚡ Unreal Engine 5 (UE5)

The C++ reader in [`cpp/`](cpp/) provides native integration into Unreal Engine 5 (UE 5.3, 5.4, 5.5+):

```cpp
#include "Py4sReader.h"
#include "Chaos/TriangleMeshImplicitObject.h"

// 1. Load the single .py4s container from disk or pak
PyGrassReal::FPy4sContainer Container;
if (PyGrassReal::FPy4sReader::UnpackFromFile(TEXT("Content/Models/character.py4s"), Container))
{
    UE_LOG(LogTemp, Log, TEXT("Loaded 4DGS: %d frames at %f FPS"), 
        Container.Metadata.TotalFrames, Container.Metadata.FPS);

    // 2. Pass Canonical 3DGS Base (Container.SpzData) to Niagara / Splat Render Component
    MySplatComponent->LoadCanonicalBase(Container.SpzData.GetData(), Container.SpzData.Num());

    // 3. Upload HexPlane deformation weights to GPU Compute Shader
    MySplatComponent->InitHexPlaneDeformation(Container.DeformationData.GetData(), Container.DeformationData.Num());

    // 4. Register Chaos deformable collision mesh (Container.ColliderData)
    MyCollisionComponent->InitializeDeformableMesh(Container.ColliderData.GetData(), Container.ColliderData.Num());
}
```

### 2. 🎯 Unity Engine (URP & HDRP)

Use the C# reader in [`unity/Py4sReader.cs`](unity/Py4sReader.cs) to unpack and drive 4DGS motion:

```csharp
using UnityEngine;
using PyGrassReal;

public class Py4sActor : MonoBehaviour
{
    public string py4sFilePath = "Assets/Models/character.py4s";
    public ComputeShader hexPlaneDeformShader;
    
    private Py4sContainer container;
    private MeshCollider meshCollider;

    void Start()
    {
        // 1. Unpack single .py4s file
        if (Py4sReader.UnpackFromFile(py4sFilePath, out container))
        {
            Debug.Log($"Loaded PY4S: {container.Metadata.temporal.total_frames} frames @ {container.Metadata.temporal.fps} FPS");

            // 2. Setup Canonical 3DGS Base ComputeBuffer
            InitGaussianBuffers(container.SpzData);

            // 3. Upload HexPlane feature textures / weights to Compute Shader
            hexPlaneDeformShader.SetFloats("_Duration", container.Metadata.temporal.duration_seconds);
        }
    }

    void Update()
    {
        // 4. Deform Gaussians & MeshCollider synchronously at current playback time
        float currentTime = Time.time % container.Metadata.temporal.duration_seconds;
        hexPlaneDeformShader.SetFloat("_Timestamp", currentTime);
        hexPlaneDeformShader.Dispatch(0, Mathf.CeilToInt(gaussianCount / 256f), 1, 1);
        
        // 5. Update physical collision vertices in real-time
        UpdateDeformedCollider(currentTime);
    }
}
```

### 3. 🐍 Python SDK (Inference & Deep Learning)

```python
from py4s_codec import Py4sCodec, Py4sContainer

# Unpack a .py4s file
container = Py4sCodec.unpack_file("character_motion.py4s")
print(f"Total Frames: {container.metadata['temporal']['total_frames']}")
print(f"FPS: {container.metadata['temporal']['fps']}")
print(f"Canonical 3DGS Size: {len(container.spz_data):,} bytes")
print(f"HexPlane Size: {len(container.deformation_data):,} bytes")

# Pack a modified or newly trained 4DGS model
packed_bytes = Py4sCodec.pack(container)
with open("output_model.py4s", "wb") as f:
    f.write(packed_bytes)
```

### 4. 🌐 Web & TypeScript (Three.js / WebGL / WebGPU)

```typescript
import { Py4sCodec, isPy4sBuffer, getPy4sBaseVisual } from './py4sCodec';

const response = await fetch('character_motion.py4s');
const arrayBuffer = await response.arrayBuffer();

if (isPy4sBuffer(arrayBuffer)) {
  const container = Py4sCodec.unpack(arrayBuffer);
  console.log('4DGS Metadata:', container.metadata);
  
  // Extract base visual for immediate Three.js 3DGS renderer
  const visual = getPy4sBaseVisual(arrayBuffer);
  console.log(`Base Visual Format: ${visual.format}`);
}
```

---

## 📊 File Size & Performance Comparison

| Asset Type | Raw 4DGS Keyframes (90 PLY frames) | Uncompressed `.py4s` (Raw PLY) | `.py4s` with Adobe SPZ v4 | Size Reduction | Target Engines |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Cybernetic Character** | 1,080 MB | 11.87 MB | **2.24 MB** | **-99.8% vs raw frames** | Unreal Engine 5, Unity, Web |
| **Robotic Arm 3D Printing**| 1,260 MB | 14.12 MB | **2.68 MB** | **-99.8% vs raw frames** | Unreal Engine 5, Unity, Web |

---

## 📜 Intellectual Property & Copyright Recordation

* **DIP Thailand Registration:** Recorded with the Department of Intellectual Property (DIP), Thailand, under the Computer Program category. See [docs/COPYRIGHT_RECORDATION_GUIDE.md](docs/COPYRIGHT_RECORDATION_GUIDE.md) for full application templates.
* **International Protection:** Protected automatically across 181 countries under the **Berne Convention**.
* **MIME Media Type:** `model/vnd.pygrassreal.py4s` (Registered with IANA draft in [docs/IANA_MIME_REGISTRATION_DRAFT.md](docs/IANA_MIME_REGISTRATION_DRAFT.md)).
* **License:** Permissive open-source [MIT License](LICENSE).
