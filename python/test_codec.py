# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
# flake8: noqa
#!/usr/bin/env python3
import os
import sys
import json
import tempfile
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from py4s_codec import Py4sContainer, HEADER_MAGIC, VERSION_MAJOR, VERSION_MINOR

class TestPy4sCodec(unittest.TestCase):
    def test_pack_unpack_cycle(self):
        fake_spz = b"SPZ_GAUSSIAN_DATA_CANONICAL_POINTS"
        fake_deform = b"HEXPLANE_MLP_WEIGHTS_BIN_DATA_V1"
        fake_collider = b"GLTF_DEFORMABLE_PHYSICS_COLLIDER"
        fake_meta = {
            "format": "py4s",
            "version": f"{VERSION_MAJOR}.{VERSION_MINOR}.0",
            "temporal": {"duration_seconds": 2.5, "fps": 30, "total_frames": 75},
            "generator": "Kinnaree 1.0 (4DGS)"
        }
        fake_thumb = b"RIFF_ANIMATED_WEBP_PREVIEW"

        packed = Py4sContainer.pack(fake_spz, fake_deform, fake_collider, fake_meta, fake_thumb)
        self.assertTrue(packed.startswith(HEADER_MAGIC))
        self.assertGreater(len(packed), 128)

        # Unpack
        container = Py4sContainer.unpack(packed)
        self.assertEqual(container.version_major, VERSION_MAJOR)
        self.assertEqual(container.version_minor, VERSION_MINOR)
        self.assertEqual(container.spz_data, fake_spz)
        self.assertEqual(container.deformation_data, fake_deform)
        self.assertEqual(container.collider_data, fake_collider)
        self.assertEqual(container.metadata["generator"], "Kinnaree 1.0 (4DGS)")
        self.assertEqual(container.metadata["temporal"]["fps"], 30)
        self.assertEqual(container.thumbnail_data, fake_thumb)

if __name__ == "__main__":
    unittest.main()
