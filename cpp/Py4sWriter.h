// Copyright 2026 PyGrassReal AI. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Py4sFormat.h"

namespace PyGrassReal
{
	class PYGRASSREAL4D_API FPy4sWriter
	{
	public:
		/**
		 * Packs an FPy4sContainer into a contiguous binary byte buffer.
		 */
		static bool PackToBuffer(const FPy4sContainer& InContainer, TArray<uint8>& OutBuffer);

		/**
		 * Packs an FPy4sContainer and writes it directly to disk at FilePath.
		 */
		static bool WriteToFile(const FPy4sContainer& InContainer, const FString& FilePath);
	};
}

