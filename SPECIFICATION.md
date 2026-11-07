# 📦 ข้อกำหนดโครงสร้างไฟล์ PyGrassReal 4D Dynamic Splat (`.py4s`)
### มาตรฐานสินทรัพย์ดิจิทัล 4D Dynamic Gaussian Splatting และฟิสิกส์การชนแบบเปลี่ยนรูปตามเวลา

> **ลิขสิทธิ์**: Copyright (c) 2026 **PyGrassReal AI** (https://pygrassreal.ai). All Rights Reserved.  
> **แบรนด์/ผู้พัฒนา**: **PyGrassReal**  
> **เอนจิ้น AI ผู้สร้าง**: **Kinnaree 1.0** — Video-to-4DGS Spatial Computing Engine  
> **ชื่อฟอร์แมต**: PyGrassReal 4D Splat Single Container (`.py4s`)  
> **MIME Media Type**: `model/vnd.pygrassreal.py4s`  
> **เวอร์ชันสเปก**: `1.0.0`  
> **Magic String**: `"PY4S"` (`0x50 0x59 0x34 0x53`)  
> **Endianness**: Little-Endian (LE)  
> **ขนาด Header**: 128 Bytes  
> **เป้าหมายการใช้งาน**: Unreal Engine 5, Unity (URP/HDRP), WebGL/WebGPU, Deep Learning Pipelines  

---

## 1. วัตถุประสงค์ (Purpose)

`.py4s` เป็น Single-Container Asset Format มาตรฐานทางการของ **PyGrassReal AI** ที่สร้างขึ้นเพื่อแก้ไขปัญหาคอขวดของการใช้งาน 4D Gaussian Splatting (4DGS) ในเอนจิ้นเกมระดับอุตสาหกรรม โดยรวมองค์ประกอบทั้ง 4 มิติไว้ในไฟล์ไบนารีเดียว:

1. **Canonical 3DGS Base Layer**: จุดตั้งต้น 3 มิติในท่าพัก ($t=0$) บีบอัดความหนาแน่นสูงด้วยอัลกอริทึม Adobe SPZ v4 ลดขนาดไฟล์ลงได้ถึง **85%** โดยคงจุด Gaussians ไว้ครบ 100% ไม่มีการตัดทอน
2. **HexPlane Neural Deformation Layer**: ระนาบคุณลักษณะโครงข่ายประสาท 6 ทิศทาง ($XY, XZ, YZ, XT, YT, ZT$) พร้อมโครงข่ายประสาทเทียมขนาดเล็ก (MLP) ทำนายการกระจัดของตำแหน่ง ($\Delta \mu$), การหมุนควอเทอร์เนียน ($\Delta q$) และขนาด ($\Delta s$) ของทุก Gaussian ตามเวลา $t$
3. **Synchronized Deformable Physics Layer**: โครงสร้างเรขาคณิตการชน (GLB Hitbox) ที่เปลี่ยนรูปตามเวลาแบบ Synchronized อิงอัลกอริทึม K-Nearest Neighbors ($K=4$) และ Inverse Distance Weighting (IDW) คำนวณเสร็จภายใน $<2\text{ms}$ ต่อเฟรมที่ 30/60 FPS
4. **Spatiotemporal Metadata Layer**: ชุดข้อมูลพารามิเตอร์เวลา อัตราเฟรม (FPS) ระยะเวลารวม ขอบเขตพิกัด และกฎการวนซ้ำ (Looping)
5. **Animated Preview Layer** *(Optional)*: ชุดข้อมูลภาพเคลื่อนไหวตัวอย่าง (WebP/MP4) สำหรับการแสดงผลพรีวิวทันทีโดยไม่ต้องโหลดโมเดลทั้งหมด

รวมจบสมบูรณ์ในคอนเทนเนอร์เดียว สามารถลากเข้าสู่ **Unreal Engine 5** หรือ **Unity** เพื่อแสดงผลภาพ 4DGS เคลื่อนไหวพร้อมรองรับการชนทางฟิสิกส์ 1:1 ได้ทันทีโดยไม่ต้อง Rigging หรือตั้งค่าเพิ่มเติม

---

## 2. โครงสร้างหน่วยความจำ (Binary Layout)

```text
┌────────────────────────────────────────────────────────┐
│             PY4S File Header (128 Bytes)               │  Offset 0x00
├────────────────────────────────────────────────────────┤
│ Section 1: Canonical 3DGS Layer (SPZ / PLY Base)       │  Offset = SpzOffset (ปกติ 0x80)
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

## 3. ตารางโครงสร้าง Header (128 Bytes)

ข้อมูลตัวเลขหลายไบต์ทั้งหมดถูกจัดเก็บในรูปแบบ **Little-Endian (LE)**:

| Offset (Hex) | ขนาด (Bytes) | ชนิดข้อมูล | ชื่อฟิลด์ | คำอธิบาย |
|---|---|---|---|---|
| `0x00` | 4 | `char[4]` | `Magic` | ต้องเป็น `"PY4S"` (`0x50 0x59 0x34 0x53`) |
| `0x04` | 2 | `uint16` | `VersionMajor` | เวอร์ชันหลัก (ปัจจุบัน = `1`) |
| `0x06` | 2 | `uint16` | `VersionMinor` | เวอร์ชันย่อย (ปัจจุบัน = `0`) |
| `0x08` | 4 | `uint32` | `SectionCount` | จำนวน sections (ปกติ = `4` หรือ `5`) |
| `0x0C` | 4 | `uint32` | `Flags` | บิตแฟล็กการเข้ารหัสและการบีบอัดข้อมูล |
| `0x10` | 8 | `uint64` | `SpzOffset` | Byte offset จุดเริ่มต้นของ Canonical 3DGS Base |
| `0x18` | 8 | `uint64` | `SpzSize` | ขนาดของ Canonical 3DGS Base (bytes) |
| `0x20` | 8 | `uint64` | `DeformationOffset`| Byte offset จุดเริ่มต้นของ HexPlane Deformation |
| `0x28` | 8 | `uint64` | `DeformationSize`  | ขนาดของ HexPlane Deformation (bytes) |
| `0x30` | 8 | `uint64` | `ColliderOffset`   | Byte offset จุดเริ่มต้นของ Deformable Collider |
| `0x38` | 8 | `uint64` | `ColliderSize`     | ขนาดของ Deformable Collider (bytes) |
| `0x40` | 8 | `uint64` | `MetadataOffset`   | Byte offset จุดเริ่มต้นของ Spatiotemporal Metadata |
| `0x48` | 8 | `uint64` | `MetadataSize`     | ขนาดของ Metadata JSON (bytes) |
| `0x50` | 8 | `uint64` | `ThumbnailOffset`  | Byte offset ของ Animated Preview (0 ถ้าไม่มี) |
| `0x58` | 8 | `uint64` | `ThumbnailSize`    | ขนาดของ Animated Preview (0 ถ้าไม่มี) |
| `0x60` | 32 | `uint8[32]` | `Reserved`      | สงวนไว้สำหรับส่วนขยายอนาคต (zero padding) |

### ความหมายของบิตแฟล็ก (`Flags` 32-bit):
* `0x0001` - `PY4S_FLAG_SPZ_ZSTD`: ส่วน Canonical 3DGS Base บีบอัดด้วย Adobe SPZ / Zstandard
* `0x0002` - `PY4S_FLAG_HEXPLANE_DEFORM`: มีข้อมูล HexPlane Neural Deformation Weights
* `0x0004` - `PY4S_FLAG_COLLIDER_DEFORMABLE`: เรขาคณิตการชนถูกแมปพร้อมเปลี่ยนรูปตามเวลาแบบ 1:1
* `0x0010` - `PY4S_FLAG_HAS_ANIMATED_PREVIEW`: มีชุดข้อมูลภาพเคลื่อนไหวพรีวิวประกอบ

---

## 4. โครงสร้าง JSON Metadata (Section 4)

```json
{
  "format": "py4s",
  "version": "1.0.0",
  "generator": "Kinnaree 1.0 Video-to-4DGS",
  "temporal": {
    "total_frames": 90,
    "fps": 30.0,
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
    "plane_resolution": [64, 64],
    "hidden_dim": 64
  },
  "asset": {
    "name": "kinnaree_warrior_motion",
    "bounds": {
      "min": [-0.5, -0.8, -0.5],
      "max": [0.5, 0.8, 0.5]
    }
  }
}
```

---

## 5. การจัดตำแหน่งพิกัดและสเกล 4 มิติ (Spatiotemporal Alignment)

1. **ระบบพิกัดพื้นฐาน**: ใช้ระบบพิกัด Right-Handed Cartesian ($Y$-Up หรือ $Z$-Up ตาม Metadata) ในสเกลเมตร (Metric Meters)
2. **ความสอดคล้องระหว่าง Splat และ Collider**: จุดยอดของ Collision Mesh แชร์จุดกำเนิดและหน่วยสเกลเดียวกันกับ Canonical 3DGS Base 1:1 ทำให้สามารถส่งผ่านเวกเตอร์การกระจัด $\Delta \vec{p}(t)$ จาก Gaussians ข้างเคียงได้ทันทีโดยไม่ต้องชดเชย Matrix เพิ่มเติม
3. **การประมวลผลบน GPU**: ใน Unreal Engine 5 และ Unity ให้โหลดข้อมูล Canonical 3DGS Base และ HexPlane แผ่นระนาบเข้าสู่ GPU VRAM จากนั้นใช้ Compute Shader คำนวณเวกเตอร์ตำแหน่ง $\mu(t)$, ควอเทอร์เนียน $q(t)$ และสเกล $s(t)$ ต่อเฟรม

---

## 6. ทรัพย์สินทางปัญญาและการคุ้มครองทางกฎหมาย (Intellectual Property & Legal Protection)

* **การแจ้งข้อมูลลิขสิทธิ์**: ยื่นแจ้งข้อมูลลิขสิทธิ์ต่อ **กรมทรัพย์สินทางปัญญา (DIP) กระทรวงพาณิชย์ ประเทศไทย** ในประเภทงานวรรณกรรม (โปรแกรมคอมพิวเตอร์) ตามแบบ ลข.01 (ดูรายละเอียดใน [docs/COPYRIGHT_RECORDATION_GUIDE.md](docs/COPYRIGHT_RECORDATION_GUIDE.md))
* **การคุ้มครองระดับสากล**: ได้รับความคุ้มครองอัตโนมัติใน 181 ประเทศภาคีสมาชิกตาม **อนุสัญญากรุงเบิร์น (Berne Convention)**
* **MIME Media Type**: ยื่นร่างลงทะเบียนกับ **Internet Assigned Numbers Authority (IANA)** ในชื่อ `model/vnd.pygrassreal.py4s`
* **สัญญาอนุญาต**: เผยแพร่แบบโอเพนซอร์สภายใต้สัญญาอนุญาต [MIT License](LICENSE)
