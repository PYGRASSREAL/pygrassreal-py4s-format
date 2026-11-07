// Copyright 2026 PyGrassReal AI. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Py4sFormat.h"

namespace PyGrassReal
{
	class PYGRASSREAL4D_API FPy4sReader
	{
	public:
		/**
		 * Quickly checks whether a memory buffer begins with the "PY4S" magic header.
		 */
		static bool IsPy4sBuffer(const uint8* Buffer, int64 BufferSize);

		/**
		 * Unpacks an in-memory .py4s binary buffer into a structured FPy4sContainer.
		 */
		static bool UnpackFromBuffer(const uint8* Buffer, int64 BufferSize, FPy4sContainer& OutContainer);

		/**
		 * Loads a .py4s file from disk and unpacks it into OutContainer.
		 */
		static bool UnpackFromFile(const FString& FilePath, FPy4sContainer& OutContainer);
	};
}

