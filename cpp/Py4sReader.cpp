// Copyright 2026 PyGrassReal AI. All Rights Reserved.

#include "Py4sReader.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace PyGrassReal
{
	bool FPy4sReader::IsPy4sBuffer(const uint8* Buffer, int64 BufferSize)
	{
		if (!Buffer || BufferSize < sizeof(FPy4sFileHeader))
		{
			return false;
		}

		return Buffer[0] == 'P' && Buffer[1] == 'Y' && Buffer[2] == '4' && Buffer[3] == 'S';
	}

	bool FPy4sReader::UnpackFromBuffer(const uint8* Buffer, int64 BufferSize, FPy4sContainer& OutContainer)
	{
		if (!IsPy4sBuffer(Buffer, BufferSize))
		{
			return false;
		}

		FMemory::Memcpy(&OutContainer.Header, Buffer, sizeof(FPy4sFileHeader));

		if (OutContainer.Header.VersionMajor > PY4S_VERSION_MAJOR)
		{
			return false;
		}

		// Validate Canonical 3DGS Base section
		if (OutContainer.Header.SpzSize > 0)
		{
			if (OutContainer.Header.SpzOffset + OutContainer.Header.SpzSize > (uint64)BufferSize)
			{
				return false;
			}
			OutContainer.SpzData.SetNumUninitialized(OutContainer.Header.SpzSize);
			FMemory::Memcpy(OutContainer.SpzData.GetData(), Buffer + OutContainer.Header.SpzOffset, OutContainer.Header.SpzSize);
		}

		// Validate HexPlane Neural Deformation section
		if (OutContainer.Header.DeformationSize > 0)
		{
			if (OutContainer.Header.DeformationOffset + OutContainer.Header.DeformationSize > (uint64)BufferSize)
			{
				return false;
			}
			OutContainer.DeformationData.SetNumUninitialized(OutContainer.Header.DeformationSize);
			FMemory::Memcpy(OutContainer.DeformationData.GetData(), Buffer + OutContainer.Header.DeformationOffset, OutContainer.Header.DeformationSize);
		}

		// Validate Deformable Collider section
		if (OutContainer.Header.ColliderSize > 0)
		{
			if (OutContainer.Header.ColliderOffset + OutContainer.Header.ColliderSize > (uint64)BufferSize)
			{
				return false;
			}
			OutContainer.ColliderData.SetNumUninitialized(OutContainer.Header.ColliderSize);
			FMemory::Memcpy(OutContainer.ColliderData.GetData(), Buffer + OutContainer.Header.ColliderOffset, OutContainer.Header.ColliderSize);
		}

		// Validate Metadata JSON section
		if (OutContainer.Header.MetadataSize > 0)
		{
			if (OutContainer.Header.MetadataOffset + OutContainer.Header.MetadataSize > (uint64)BufferSize)
			{
				return false;
			}
			TArray<uint8> MetaBytes;
			MetaBytes.SetNumUninitialized(OutContainer.Header.MetadataSize + 1);
			FMemory::Memcpy(MetaBytes.GetData(), Buffer + OutContainer.Header.MetadataOffset, OutContainer.Header.MetadataSize);
			MetaBytes[OutContainer.Header.MetadataSize] = 0; // Null terminator
			OutContainer.MetadataJson = UTF8_TO_TCHAR(reinterpret_cast<const char*>(MetaBytes.GetData()));
			OutContainer.Metadata.FromJson(OutContainer.MetadataJson);
		}

		// Validate Animated Preview Thumbnail section
		if (OutContainer.Header.ThumbnailSize > 0)
		{
			if (OutContainer.Header.ThumbnailOffset + OutContainer.Header.ThumbnailSize > (uint64)BufferSize)
			{
				return false;
			}
			OutContainer.ThumbnailData.SetNumUninitialized(OutContainer.Header.ThumbnailSize);
			FMemory::Memcpy(OutContainer.ThumbnailData.GetData(), Buffer + OutContainer.Header.ThumbnailOffset, OutContainer.Header.ThumbnailSize);
		}

		return true;
	}

	bool FPy4sReader::UnpackFromFile(const FString& FilePath, FPy4sContainer& OutContainer)
	{
		TArray<uint8> FileBytes;
		if (!FFileHelper::LoadFileToArray(FileBytes, *FilePath))
		{
			return false;
		}

		return UnpackFromBuffer(FileBytes.GetData(), FileBytes.Num(), OutContainer);
	}
}
