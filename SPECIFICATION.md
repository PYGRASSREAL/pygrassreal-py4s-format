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

1. **Visual Layer**: ชุดข้อมูลแสดงผล 4D Dynamic Gaussian Splatting บีบอัดด้วย SPZ ลดขนาดไฟล์ลงได้ถึง **85%** โดยคงคุณภาพครบถ้วน
2. **Deformation Layer**: ชุดข้อมูลการเคลื่อนไหวและการเปลี่ยนรูปตามเวลา (Temporal Motion & Deformation)
3. **Physics Layer**: โครงเรขาคณิตการชน (Collision Mesh / Hitbox) ที่ขยับเปลี่ยนรูปตามตัวละครแบบเรียลไทม์ 1:1
4. **Metadata Layer**: ชุดข้อมูลพารามิเตอร์เวลา อัตราเฟรม (FPS) ระยะเวลา และการวนซ้ำ
5. **Thumbnail Layer** *(Optional)*: ชุดข้อมูลภาพเคลื่อนไหวตัวอย่างสำหรับการแสดงผลพรีวิวทันที

รวมจบสมบูรณ์ในคอนเทนเนอร์เดียว สามารถลากเข้าสู่ **Unreal Engine 5** หรือ **Unity** เพื่อแสดงผลภาพ 4DGS เคลื่อนไหวพร้อมรองรับการชนทางฟิสิกส์ 1:1 ได้ทันทีโดยไม่ต้อง Rigging หรือตั้งค่าเพิ่มเติม

---

## 2. โครงสร้างหน่วยความจำ (Binary Layout)

```text
┌────────────────────────────────────────────────────────┐
│             PY4S File Header (128 Bytes)               │  Offset 0x00
├────────────────────────────────────────────────────────┤
│     Section 1: Visual Layer (Compressed 4DGS Payload)  │  Offset = SpzOffset (ปกติ 0x80)
├────────────────────────────────────────────────────────┤
│     Section 2: Deformation Layer (Temporal Motion)     │  Offset = DeformationOffset
├────────────────────────────────────────────────────────┤
│     Section 3: Physics Layer (Deformable Collider)     │  Offset = ColliderOffset
├────────────────────────────────────────────────────────┤
│     Section 4: Metadata Layer (Spatiotemporal)         │  Offset = MetadataOffset
├────────────────────────────────────────────────────────┤
│     Section 5: Visual Preview Layer (Optional Preview) │  Offset = ThumbnailOffset
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
| `0x10` | 8 | `uint64` | `SpzOffset` | Byte offset จุดเริ่มต้นของ Visual Layer (Compressed 4DGS Payload) |
| `0x18` | 8 | `uint64` | `SpzSize` | ขนาดของ Visual Layer (bytes) |
| `0x20` | 8 | `uint64` | `DeformationOffset`| Byte offset จุดเริ่มต้นของ Deformation Layer (Temporal Motion) |
| `0x28` | 8 | `uint64` | `DeformationSize`  | ขนาดของ Deformation Layer (bytes) |
| `0x30` | 8 | `uint64` | `ColliderOffset`   | Byte offset จุดเริ่มต้นของ Physics Layer (Deformable Collider) |
| `0x38` | 8 | `uint64` | `ColliderSize`     | ขนาดของ Physics Layer (bytes) |
| `0x40` | 8 | `uint64` | `MetadataOffset`   | Byte offset จุดเริ่มต้นของ Metadata Layer (Spatiotemporal) |
| `0x48` | 8 | `uint64` | `MetadataSize`     | ขนาดของ Metadata Layer (bytes) |
| `0x50` | 8 | `uint64` | `ThumbnailOffset`  | Byte offset ของ Visual Preview Layer (0 ถ้าไม่มี) |
| `0x58` | 8 | `uint64` | `ThumbnailSize`    | ขนาดของ Visual Preview Layer (0 ถ้าไม่มี) |
| `0x60` | 32 | `uint8[32]` | `Reserved`      | สงวนไว้สำหรับส่วนขยายอนาคต (zero padding) |

### ความหมายของบิตแฟล็ก (`Flags` 32-bit):
* `0x0001` - `PY4S_FLAG_SPZ_ZSTD`: บิตแฟล็กการบีบอัดข้อมูลความหนาแน่นสูง
* `0x0002` - `PY4S_FLAG_HEXPLANE_DEFORM`: บิตแฟล็กระบุชุดข้อมูลการเคลื่อนไหวตามเวลา
* `0x0004` - `PY4S_FLAG_COLLIDER_DEFORMABLE`: บิตแฟล็กโครงเรขาคณิตการชนเปลี่ยนรูปตามเวลา
* `0x0010` - `PY4S_FLAG_HAS_ANIMATED_PREVIEW`: บิตแฟล็กมีชุดข้อมูลภาพตัวอย่างเคลื่อนไหว

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
    "format": "py4s_base",
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
