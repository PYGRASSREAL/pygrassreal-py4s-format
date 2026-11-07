// Copyright 2026 PyGrassReal AI. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Dom/JsonObject.h"

namespace PyGrassReal
{
	/** Magic string bytes: 'P', 'Y', '4', 'S' */
	static constexpr uint8 PY4S_MAGIC_BYTES[4] = { 'P', 'Y', '4', 'S' };
	static constexpr uint32 PY4S_MAGIC_UINT32 = 0x53345950; // Little-endian 'PY4S'

	static constexpr uint16 PY4S_VERSION_MAJOR = 1;
	static constexpr uint16 PY4S_VERSION_MINOR = 0;

	static constexpr uint32 PY4S_FLAG_NONE = 0x0;
	static constexpr uint32 PY4S_FLAG_SPZ_ZSTD = 0x1;
	static constexpr uint32 PY4S_FLAG_HEXPLANE_DEFORM = 0x2;
	static constexpr uint32 PY4S_FLAG_COLLIDER_DEFORMABLE = 0x4;
	static constexpr uint32 PY4S_FLAG_HAS_ANIMATED_PREVIEW = 0x10;

	#pragma pack(push, 1)
	/**
	 * 128-Byte Binary Header for .py4s 4D Dynamic Splat Container files
	 */
	struct FPy4sFileHeader
	{
		uint8 Magic[4];             // 0x00: "PY4S"
		uint16 VersionMajor;        // 0x04: 1
		uint16 VersionMinor;        // 0x06: 0
		uint32 SectionCount;        // 0x08: Number of active sections (usually 4 or 5)
		uint32 Flags;               // 0x0C: Bitwise format flags
		uint64 SpzOffset;           // 0x10: Byte offset to Canonical 3DGS Base (.spz/.ply)
		uint64 SpzSize;             // 0x18: Size in bytes of Canonical 3DGS Base
		uint64 DeformationOffset;   // 0x20: Byte offset to HexPlane Neural Deformation payload
		uint64 DeformationSize;     // 0x28: Size in bytes of Deformation payload
		uint64 ColliderOffset;      // 0x30: Byte offset to Deformable Physics Collider (.glb)
		uint64 ColliderSize;        // 0x38: Size in bytes of Collider payload
		uint64 MetadataOffset;      // 0x40: Byte offset to Spatiotemporal Metadata JSON
		uint64 MetadataSize;        // 0x48: Size in bytes of Metadata JSON
		uint64 ThumbnailOffset;     // 0x50: Byte offset to Animated Preview (0 if none)
		uint64 ThumbnailSize;       // 0x58: Size in bytes of Animated Preview (0 if none)
		uint8 Reserved[32];         // 0x60: 32 bytes reserved for future extensions

		FPy4sFileHeader()
		{
			FMemory::Memzero(this, sizeof(FPy4sFileHeader));
			Magic[0] = 'P';
			Magic[1] = 'Y';
			Magic[2] = '4';
			Magic[3] = 'S';
			VersionMajor = PY4S_VERSION_MAJOR;
			VersionMinor = PY4S_VERSION_MINOR;
		}

		bool IsValid() const
		{
			return Magic[0] == 'P' && Magic[1] == 'Y' && Magic[2] == '4' && Magic[3] == 'S';
		}
	};
	#pragma pack(pop)

	static_assert(sizeof(FPy4sFileHeader) == 128, "FPy4sFileHeader must be exactly 128 bytes");

	/**
	 * High-level parsed Metadata stored inside Section 4 of a .py4s file
	 */
	struct PYGRASSREAL4D_API FPy4sMetadata
	{
		FString Format = TEXT("py4s");
		FString Version = TEXT("1.0.0");
		FString Generator = TEXT("Kinnaree 1.0 (4DGS)");
		FString CreatedAt;

		FString AssetName;
		int32 GaussianCount = 0;
		FBox Bounds = FBox(EForceInit::ForceInit);

		// Temporal / Animation properties
		int32 TotalFrames = 30;
		float FPS = 30.0f;
		float DurationSeconds = 1.0f;
		bool bIsLooping = true;
		FVector2D TimeRange = FVector2D(0.0f, 1.0f);

		// Deformation architecture
		FString DeformationType = TEXT("trained_hexplane_keyframes");
		FString DeformationEncoding = TEXT("K4D1");

		// Collider properties
		FString ColliderFormat = TEXT("glb");
		int32 ColliderTriangleCount = 0;
		bool bColliderDeformable = true;

		FString ToJson() const;
		bool FromJson(const FString& JsonStr);
	};

	/**
	 * In-memory Representation of a .py4s Container
	 */
	struct PYGRASSREAL4D_API FPy4sContainer
	{
		FPy4sFileHeader Header;
		TArray<uint8> SpzData;
		TArray<uint8> DeformationData;
		TArray<uint8> ColliderData;
		FString MetadataJson;
		FPy4sMetadata Metadata;
		TArray<uint8> ThumbnailData;

		bool HasDeformation() const { return DeformationData.Num() > 0; }
		bool HasCollider() const { return ColliderData.Num() > 0; }
		bool HasThumbnail() const { return ThumbnailData.Num() > 0; }
	};
}
