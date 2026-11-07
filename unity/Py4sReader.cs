// Copyright 2026 PyGrassReal AI. All Rights Reserved.
// Official PyGrassReal 4D Dynamic Splat (.py4s) Unity C# Codec
// Target: Unity 2022.3+ / 2023 / 6000 (URP & HDRP)

using System;
using System.IO;
using System.Text;
using UnityEngine;

namespace PyGrassReal
{
    [Serializable]
    public class Py4sTemporalMeta
    {
        public int total_frames;
        public float fps = 30.0f;
        public float duration_seconds = 1.0f;
        public bool is_looping = true;
        public float[] time_range;
    }

    [Serializable]
    public class Py4sMetadata
    {
        public string format = "py4s";
        public string version = "1.0.0";
        public string generator = "Kinnaree 1.0";
        public Py4sTemporalMeta temporal;
    }

    public class Py4sContainer
    {
        public ushort VersionMajor;
        public ushort VersionMinor;
        public uint Flags;
        public byte[] SpzData;
        public byte[] DeformationData;
        public byte[] ColliderData;
        public string MetadataJson;
        public Py4sMetadata Metadata;
        public byte[] ThumbnailData;
    }

    public static class Py4sReader
    {
        public const string HeaderMagic = "PY4S";
        public const int HeaderSize = 128;
        public const ushort SupportedVersionMajor = 1;

        public const uint FlagSpzZstd = 0x1;
        public const uint FlagHexPlaneDeform = 0x2;
        public const uint FlagColliderDeformable = 0x4;
        public const uint FlagHasAnimatedPreview = 0x10;

        /// <summary>
        /// Quickly checks if the given byte array begins with the 'PY4S' magic signature.
        /// </summary>
        public static bool IsPy4sBuffer(byte[] buffer)
        {
            if (buffer == null || buffer.Length < 4) return false;
            return buffer[0] == 0x50 && // 'P'
                   buffer[1] == 0x59 && // 'Y'
                   buffer[2] == 0x34 && // '4'
                   buffer[3] == 0x53;   // 'S'
        }

        /// <summary>
        /// Unpacks a .py4s binary buffer into a structured Py4sContainer.
        /// </summary>
        public static bool UnpackFromBuffer(byte[] buffer, out Py4sContainer container)
        {
            container = null;
            if (!IsPy4sBuffer(buffer) || buffer.Length < HeaderSize)
            {
                Debug.LogError("[Py4sReader] Invalid PY4S container magic or header size.");
                return false;
            }

            using (var stream = new MemoryStream(buffer))
            using (var reader = new BinaryReader(stream))
            {
                reader.BaseStream.Seek(4, SeekOrigin.Begin);
                ushort versionMajor = reader.ReadUInt16();
                ushort versionMinor = reader.ReadUInt16();
                uint sectionCount = reader.ReadUInt32();
                uint flags = reader.ReadUInt32();

                ulong spzOffset = reader.ReadUInt64();
                ulong spzSize = reader.ReadUInt64();
                ulong deformOffset = reader.ReadUInt64();
                ulong deformSize = reader.ReadUInt64();
                ulong colliderOffset = reader.ReadUInt64();
                ulong colliderSize = reader.ReadUInt64();
                ulong metaOffset = reader.ReadUInt64();
                ulong metaSize = reader.ReadUInt64();
                ulong thumbOffset = reader.ReadUInt64();
                ulong thumbSize = reader.ReadUInt64();

                if (spzSize == 0 || spzOffset + spzSize > (ulong)buffer.Length)
                {
                    Debug.LogError("[Py4sReader] Corrupted or missing canonical 3DGS visual section.");
                    return false;
                }

                container = new Py4sContainer
                {
                    VersionMajor = versionMajor,
                    VersionMinor = versionMinor,
                    Flags = flags,
                    SpzData = new byte[spzSize],
                    DeformationData = deformSize > 0 ? new byte[deformSize] : null,
                    ColliderData = colliderSize > 0 ? new byte[colliderSize] : null,
                    ThumbnailData = thumbSize > 0 ? new byte[thumbSize] : null
                };

                Buffer.BlockCopy(buffer, (int)spzOffset, container.SpzData, 0, (int)spzSize);
                if (deformSize > 0) Buffer.BlockCopy(buffer, (int)deformOffset, container.DeformationData, 0, (int)deformSize);
                if (colliderSize > 0) Buffer.BlockCopy(buffer, (int)colliderOffset, container.ColliderData, 0, (int)colliderSize);
                if (thumbSize > 0) Buffer.BlockCopy(buffer, (int)thumbOffset, container.ThumbnailData, 0, (int)thumbSize);

                if (metaSize > 0 && metaOffset + metaSize <= (ulong)buffer.Length)
                {
                    container.MetadataJson = Encoding.UTF8.GetString(buffer, (int)metaOffset, (int)metaSize);
                    try
                    {
                        container.Metadata = JsonUtility.FromJson<Py4sMetadata>(container.MetadataJson);
                    }
                    catch (Exception ex)
                    {
                        Debug.LogWarning($"[Py4sReader] Failed to parse JSON metadata: {ex.Message}");
                    }
                }

                return true;
            }
        }

        /// <summary>
        /// Reads a .py4s file from disk and unpacks it into a Py4sContainer.
        /// </summary>
        public static bool UnpackFromFile(string filePath, out Py4sContainer container)
        {
            container = null;
            if (!File.Exists(filePath))
            {
                Debug.LogError($"[Py4sReader] File not found: {filePath}");
                return false;
            }

            try
            {
                byte[] bytes = File.ReadAllBytes(filePath);
                return UnpackFromBuffer(bytes, out container);
            }
            catch (Exception ex)
            {
                Debug.LogError($"[Py4sReader] Exception reading {filePath}: {ex.Message}");
                return false;
            }
        }
    }
}

