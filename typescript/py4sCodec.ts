/**
 * PyGrassReal 4D Dynamic Splat (.py4s) Web & TypeScript Codec
 * Single container packing:
 * 1. Canonical 3DGS base (.spz)
 * 2. HexPlane Neural Deformation Weights
 * 3. Deformable Physics Collider
 * 4. JSON Metadata (temporal, FPS, deformation bounds)
 * 5. Optional Animated Preview
 */

export const PY4S_HEADER_MAGIC = 'PY4S';
export const PY4S_HEADER_SIZE = 128;
export const PY4S_VERSION_MAJOR = 1;
export const PY4S_VERSION_MINOR = 0;

export const PY4S_FLAG_NONE = 0x0;
export const PY4S_FLAG_SPZ_ZSTD = 0x1;
export const PY4S_FLAG_HEXPLANE_DEFORM = 0x2;
export const PY4S_FLAG_COLLIDER_DEFORMABLE = 0x4;
export const PY4S_FLAG_HAS_ANIMATED_PREVIEW = 0x10;

export function isPy4sBuffer(buf: ArrayBuffer | ArrayBufferView | null | undefined): boolean {
  if (!buf) return false;
  const byteLength = 'byteLength' in buf ? buf.byteLength : 0;
  if (byteLength < 4) return false;
  const uint8 = 'buffer' in buf
    ? new Uint8Array(buf.buffer, buf.byteOffset, Math.min(4, buf.byteLength))
    : new Uint8Array((buf as ArrayBuffer).slice(0, 4));
  return uint8[0] === 0x50 && uint8[1] === 0x59 && uint8[2] === 0x34 && uint8[3] === 0x53; // 'PY4S'
}

export interface Py4sMetadata {
  format: 'py4s';
  version: string;
  generator?: string;
  created?: string;
  temporal?: {
    total_frames: number;
    fps: number;
    duration_seconds: number;
    is_looping: boolean;
    time_range: [number, number];
  };
  asset?: {
    name: string;
    gaussian_count?: number;
    bounds?: {
      min: [number, number, number];
      max: [number, number, number];
    };
  };
  deformation?: {
    type: string;
    plane_resolution?: [number, number];
    hidden_dim?: number;
  };
  canonical_3dgs?: {
    gaussian_count?: number;
    format?: string;
    sh_degree?: number;
    coordinate_system?: string;
    reconstruction?: string;
    size_bytes?: number;
    [key: string]: unknown;
  };
  [key: string]: unknown;
}

export interface Py4sContainerData {
  spzData: Uint8Array;
  deformationData?: Uint8Array;
  colliderData?: Uint8Array;
  metadata: Py4sMetadata;
  thumbnailData?: Uint8Array;
}

export class Py4sCodec {
  /**
   * Unpacks a .py4s binary buffer into constituent components.
   */
  public static unpack(buffer: ArrayBuffer | Uint8Array): Py4sContainerData {
    const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    if (bytes.byteLength < PY4S_HEADER_SIZE) {
      throw new Error(`Invalid PY4S buffer: size ${bytes.byteLength} < ${PY4S_HEADER_SIZE}`);
    }

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);

    // Validate Magic 'PY4S'
    if (
      bytes[0] !== 0x50 || // 'P'
      bytes[1] !== 0x59 || // 'Y'
      bytes[2] !== 0x34 || // '4'
      bytes[3] !== 0x53    // 'S'
    ) {
      throw new Error('Not a valid PY4S container (header magic mismatch)');
    }

    const versionMajor = view.getUint16(4, true);
    if (versionMajor > PY4S_VERSION_MAJOR) {
      throw new Error(`Unsupported PY4S version: ${versionMajor} > ${PY4S_VERSION_MAJOR}`);
    }

    const spzOffset = Number(view.getBigUint64(16, true));
    const spzSize = Number(view.getBigUint64(24, true));
    const deformOffset = Number(view.getBigUint64(32, true));
    const deformSize = Number(view.getBigUint64(40, true));
    const colliderOffset = Number(view.getBigUint64(48, true));
    const colliderSize = Number(view.getBigUint64(56, true));
    const metaOffset = Number(view.getBigUint64(64, true));
    const metaSize = Number(view.getBigUint64(72, true));
    const thumbOffset = Number(view.getBigUint64(80, true));
    const thumbSize = Number(view.getBigUint64(88, true));

    for (const [name, offset, size] of [
      ['visual', spzOffset, spzSize],
      ['deformation', deformOffset, deformSize],
      ['collider', colliderOffset, colliderSize],
      ['metadata', metaOffset, metaSize],
      ['thumbnail', thumbOffset, thumbSize],
    ] as const) {
      if (!Number.isSafeInteger(offset) || !Number.isSafeInteger(size) ||
          (size > 0 && (offset < PY4S_HEADER_SIZE || offset > bytes.byteLength - size))) {
        throw new Error(`Invalid PY4S ${name} section: outside container bounds`);
      }
    }
    if (spzSize === 0) throw new Error('PY4S container has no visual splat data');

    // Slice SPZ payload
    const spzData = bytes.slice(spzOffset, spzOffset + spzSize);

    // Slice Deformation payload
    const deformationData = deformSize > 0 ? bytes.slice(deformOffset, deformOffset + deformSize) : undefined;

    // Slice Collider payload
    const colliderData = colliderSize > 0 ? bytes.slice(colliderOffset, colliderOffset + colliderSize) : undefined;

    // Slice Thumbnail payload
    const thumbnailData = thumbSize > 0 ? bytes.slice(thumbOffset, thumbOffset + thumbSize) : undefined;

    // Decode Metadata
    let metadata: Py4sMetadata;
    try {
      if (metaSize > 0) {
        const metaBytes = bytes.slice(metaOffset, metaOffset + metaSize);
        const textDecoder = new TextDecoder('utf-8');
        metadata = JSON.parse(textDecoder.decode(metaBytes)) as Py4sMetadata;
      } else {
        metadata = {
          format: 'py4s',
          version: '1.0',
        };
      }
    } catch {
      metadata = {
        format: 'py4s',
        version: '1.0',
      };
    }

    return {
      spzData,
      deformationData,
      colliderData,
      metadata,
      thumbnailData,
    };
  }

  /**
   * Packs SPZ, Deformation, Collider, and Metadata into a single .py4s binary buffer.
   */
  public static pack(data: Py4sContainerData): Uint8Array {
    const textEncoder = new TextEncoder();
    const metaBytes = textEncoder.encode(JSON.stringify(data.metadata));

    const spzBytes = data.spzData;
    const deformBytes = data.deformationData ?? new Uint8Array(0);
    const colliderBytes = data.colliderData ?? new Uint8Array(0);
    const thumbBytes = data.thumbnailData ?? new Uint8Array(0);

    let currentOffset = PY4S_HEADER_SIZE;

    const spzOffset = BigInt(currentOffset);
    const spzSize = BigInt(spzBytes.byteLength);
    currentOffset += spzBytes.byteLength;

    const deformOffset = BigInt(currentOffset);
    const deformSize = BigInt(deformBytes.byteLength);
    currentOffset += deformBytes.byteLength;

    const colliderOffset = BigInt(currentOffset);
    const colliderSize = BigInt(colliderBytes.byteLength);
    currentOffset += colliderBytes.byteLength;

    const metaOffset = BigInt(currentOffset);
    const metaSize = BigInt(metaBytes.byteLength);
    currentOffset += metaBytes.byteLength;

    let thumbOffset = 0n;
    let thumbSize = 0n;
    let sectionCount = 4;
    const isPly = spzBytes[0] === 0x70 && spzBytes[1] === 0x6c && spzBytes[2] === 0x79;
    let flags = isPly ? 0 : PY4S_FLAG_SPZ_ZSTD;
    if (deformBytes.byteLength > 0) flags |= PY4S_FLAG_HEXPLANE_DEFORM;
    if (colliderBytes.byteLength > 0) flags |= PY4S_FLAG_COLLIDER_DEFORMABLE;

    if (thumbBytes.byteLength > 0) {
      thumbOffset = BigInt(currentOffset);
      thumbSize = BigInt(thumbBytes.byteLength);
      currentOffset += thumbBytes.byteLength;
      sectionCount = 5;
      flags |= PY4S_FLAG_HAS_ANIMATED_PREVIEW;
    }

    const output = new Uint8Array(currentOffset);
    const view = new DataView(output.buffer, output.byteOffset, output.byteLength);

    output[0] = 0x50; // 'P'
    output[1] = 0x59; // 'Y'
    output[2] = 0x34; // '4'
    output[3] = 0x53; // 'S'

    view.setUint16(4, PY4S_VERSION_MAJOR, true);
    view.setUint16(6, PY4S_VERSION_MINOR, true);
    view.setUint32(8, sectionCount, true);
    view.setUint32(12, flags, true);

    view.setBigUint64(16, spzOffset, true);
    view.setBigUint64(24, spzSize, true);
    view.setBigUint64(32, deformOffset, true);
    view.setBigUint64(40, deformSize, true);
    view.setBigUint64(48, colliderOffset, true);
    view.setBigUint64(56, colliderSize, true);
    view.setBigUint64(64, metaOffset, true);
    view.setBigUint64(72, metaSize, true);
    view.setBigUint64(80, thumbOffset, true);
    view.setBigUint64(88, thumbSize, true);

    if (spzBytes.byteLength > 0) output.set(spzBytes, Number(spzOffset));
    if (deformBytes.byteLength > 0) output.set(deformBytes, Number(deformOffset));
    if (colliderBytes.byteLength > 0) output.set(colliderBytes, Number(colliderOffset));
    if (metaBytes.byteLength > 0) output.set(metaBytes, Number(metaOffset));
    if (thumbBytes.byteLength > 0) output.set(thumbBytes, Number(thumbOffset));

    return output;
  }
}

/** The canonical visual may be PLY even though the section is named spzData. */
export function getPy4sBaseVisual(buffer: ArrayBuffer): { buffer: ArrayBuffer; format: 'ply' | 'spz' } {
  const bytes = isPy4sBuffer(buffer) ? Py4sCodec.unpack(buffer).spzData : new Uint8Array(buffer);
  const isPly = bytes[0] === 0x70 && bytes[1] === 0x6c && bytes[2] === 0x79 &&
    (bytes[3] === 0x0a || bytes[3] === 0x0d);
  if (!bytes.byteLength) throw new Error('PY4S container has no visual splat data');
  return { buffer: bytes.slice().buffer as ArrayBuffer, format: isPly ? 'ply' : 'spz' };
}

