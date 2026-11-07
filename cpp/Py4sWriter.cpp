// Copyright 2026 PyGrassReal AI. All Rights Reserved.

#include "Py4sWriter.h"
#include "Misc/FileHelper.h"

namespace PyGrassReal
{
	bool FPy4sWriter::PackToBuffer(const FPy4sContainer& InContainer, TArray<uint8>& OutBuffer)
	{
		FTCHARToUTF8 Utf8Meta(*InContainer.MetadataJson);
		const int32 MetaBytesLen = Utf8Meta.Length();

		uint64 CurrentOffset = sizeof(FPy4sFileHeader);

		FPy4sFileHeader Header;
		Header.SectionCount = 4;
		Header.Flags = PY4S_FLAG_NONE;

		// 1. Canonical 3DGS Base
		Header.SpzOffset = CurrentOffset;
		Header.SpzSize = InContainer.SpzData.Num();
		CurrentOffset += Header.SpzSize;
		if (Header.SpzSize > 0)
		{
			// Check if SPZ vs PLY
			if (InContainer.SpzData.Num() >= 3 &&
				InContainer.SpzData[0] != 'p' && InContainer.SpzData[1] != 'l' && InContainer.SpzData[2] != 'y')
			{
				Header.Flags |= PY4S_FLAG_SPZ_ZSTD;
			}
		}

		// 2. HexPlane Neural Deformation
		Header.DeformationOffset = CurrentOffset;
		Header.DeformationSize = InContainer.DeformationData.Num();
		CurrentOffset += Header.DeformationSize;
		if (Header.DeformationSize > 0)
		{
			Header.Flags |= PY4S_FLAG_HEXPLANE_DEFORM;
		}

		// 3. Deformable Collider
		Header.ColliderOffset = CurrentOffset;
		Header.ColliderSize = InContainer.ColliderData.Num();
		CurrentOffset += Header.ColliderSize;
		if (Header.ColliderSize > 0)
		{
			Header.Flags |= PY4S_FLAG_COLLIDER_DEFORMABLE;
		}

		// 4. Metadata
		Header.MetadataOffset = CurrentOffset;
		Header.MetadataSize = MetaBytesLen;
		CurrentOffset += Header.MetadataSize;

		// 5. Thumbnail / Animated Preview (Optional)
		if (InContainer.ThumbnailData.Num() > 0)
		{
			Header.ThumbnailOffset = CurrentOffset;
			Header.ThumbnailSize = InContainer.ThumbnailData.Num();
			CurrentOffset += Header.ThumbnailSize;
			Header.SectionCount = 5;
			Header.Flags |= PY4S_FLAG_HAS_ANIMATED_PREVIEW;
		}

		OutBuffer.SetNumUninitialized(CurrentOffset);
		uint8* Dest = OutBuffer.GetData();

		// Write Header
		FMemory::Memcpy(Dest, &Header, sizeof(FPy4sFileHeader));

		// Write Payloads
		if (Header.SpzSize > 0)
		{
			FMemory::Memcpy(Dest + Header.SpzOffset, InContainer.SpzData.GetData(), Header.SpzSize);
		}
		if (Header.DeformationSize > 0)
		{
			FMemory::Memcpy(Dest + Header.DeformationOffset, InContainer.DeformationData.GetData(), Header.DeformationSize);
		}
		if (Header.ColliderSize > 0)
		{
			FMemory::Memcpy(Dest + Header.ColliderOffset, InContainer.ColliderData.GetData(), Header.ColliderSize);
		}
		if (Header.MetadataSize > 0)
		{
			FMemory::Memcpy(Dest + Header.MetadataOffset, Utf8Meta.Get(), Header.MetadataSize);
		}
		if (Header.ThumbnailSize > 0)
		{
			FMemory::Memcpy(Dest + Header.ThumbnailOffset, InContainer.ThumbnailData.GetData(), Header.ThumbnailSize);
		}

		return true;
	}

	bool FPy4sWriter::WriteToFile(const FPy4sContainer& InContainer, const FString& FilePath)
	{
		TArray<uint8> PackedBytes;
		if (!PackToBuffer(InContainer, PackedBytes))
		{
			return false;
		}

		return FFileHelper::SaveArrayToFile(PackedBytes, *FilePath);
	}
}

