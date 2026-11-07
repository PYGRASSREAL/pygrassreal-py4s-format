import { describe, expect, it } from 'vitest';
import { getPy4sBaseVisual, isPy4sBuffer, Py4sCodec } from './py4sCodec';

const pack = (visual: Uint8Array) => Py4sCodec.pack({
  spzData: visual,
  deformationData: new Uint8Array([1, 2]),
  colliderData: new Uint8Array([3, 4]),
  metadata: {
    format: 'py4s',
    version: '1.0.0',
    temporal: {
      fps: 30,
      total_frames: 30,
      duration_seconds: 1,
      time_range: [0, 1],
      is_looping: true,
    },
  },
});

describe('PY4S canonical visual', () => {
  it('extracts the PLY emitted by Kinnaree without including other sections', () => {
    const ply = new TextEncoder().encode('ply\nformat binary_little_endian 1.0\nend_header\n');
    const packed = pack(ply);
    const visual = getPy4sBaseVisual(packed);
    expect(isPy4sBuffer(packed)).toBe(true);
    expect(visual.format).toBe('ply');
    expect(Array.from(new Uint8Array(visual.buffer))).toEqual(Array.from(ply));
    expect(Py4sCodec.unpack(packed).deformationData).toEqual(new Uint8Array([1, 2]));
  });

  it('also accepts CRLF PLY and legacy raw PLY responses', () => {
    const ply = new TextEncoder().encode('ply\r\nformat ascii 1.0\r\nend_header\r\n');
    expect(getPy4sBaseVisual(pack(ply)).format).toBe('ply');
    expect(getPy4sBaseVisual(ply.buffer).buffer).toEqual(ply.buffer);
  });

  it('routes a compressed canonical payload to SPZ decoding', () => {
    const spz = new Uint8Array([0x1f, 0x8b, 0x08, 0]);
    const visual = getPy4sBaseVisual(pack(spz));
    expect(visual.format).toBe('spz');
    expect(new Uint8Array(visual.buffer)).toEqual(spz);
  });

  it('rejects truncated or out of bounds sections before a renderer sees them', () => {
    const packed = pack(new Uint8Array([1, 2, 3, 4]));
    expect(() => Py4sCodec.unpack(packed.slice(0, 130))).toThrow(/bounds/);
    new DataView(packed.buffer, packed.byteOffset, packed.byteLength).setBigUint64(16, BigInt(Number.MAX_SAFE_INTEGER) + 1n, true);
    expect(() => Py4sCodec.unpack(packed)).toThrow(/bounds/);
  });

  it('rejects a missing canonical visual', () => {
    expect(() => Py4sCodec.unpack(pack(new Uint8Array()))).toThrow(/no visual/);
  });
});
