# IANA Media Type Registration Application for `model/vnd.pygrassreal.py4s`

**To:** iana-mime-comment@iana.org  
**Subject:** Registration of media type model/vnd.pygrassreal.py4s  

---

### Type name:
`model`

### Subtype name:
`vnd.pygrassreal.py4s`

### Required parameters:
None.

### Optional parameters:
* `version`: A string indicating the container format version (e.g. `1.0.0`).
* `temporal_fps`: An integer or float indicating default playback frames-per-second (e.g. `30`).

### Encoding considerations:
Binary.

### Security considerations:
A `.py4s` container encapsulates dense 3D Gaussian Splatting point coordinates, HexPlane neural deformation plane tensors or MLP weights, physics collision meshes, JSON metadata, and an optional visual preview. Parsers MUST validate byte offsets and payload sizes against the fixed 128-byte header to prevent buffer overrun vulnerabilities. No active executable code or macros are stored within the container.

### Interoperability considerations:
Designed as an open, single-container specification for real-time 4D Gaussian Splatting (4DGS) with synchronized deformable physics collision. Parsers must support IEEE-754 Little-Endian floating-point formats.

### Published specification:
https://github.com/PYGRASSREAL/pygrassreal-py4s-format/blob/main/SPECIFICATION.md

### Applications that use this media type:
* PyGrassReal AI 4D Platform (Kinnaree 1.0)
* Unreal Engine 5 via PyGrassReal 4DGS In-Engine Plugin
* WebGL / WebGPU Viewers (Three.js, Babylon.js)
* Omniverse / OpenUSD Spatial Computing Workflows

### Fragment identifier conventions:
None defined.

### Additional information:
* **Magic number(s):** ASCII `PY4S` (`0x50 0x59 0x34 0x53`) at byte offset 0.
* **File extension(s):** `.py4s`
* **Macintosh file type code(s):** None.

### Person & email address to contact for further information:
* **Name:** PyGrassReal AI Engineering Team
* **Email:** admin@pygrassreal.ai
* **Website:** https://pygrassreal.ai

### Intended usage:
COMMON

### Restrictions on usage:
None.

### Author:
PyGrassReal AI
