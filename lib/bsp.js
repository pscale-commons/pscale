/**
 * bsp.js — pure-form BSP for pscale JSON blocks.
 *
 * No tree wrapper, no tuning field, no metadata. The block IS the tree.
 * Floor derived from the underscore chain. Everything else is a walk.
 */

function floorDepth(block) {
  let node = block, depth = 0;
  while (node && typeof node === 'object' && '_' in node) {
    depth++;
    node = node._;
    if (typeof node === 'string') return depth;
  }
  return depth;
}

function parseAddress(number) {
  const s = typeof number === 'number' ? number.toFixed(10) : String(number);
  const [integer = '0', frac = ''] = s.split('.');
  const cleaned = frac.replace(/0+$/, '');
  if (integer === '0') return [...cleaned];
  return [...(integer + cleaned)];
}

function walk(block, digits) {
  const chain = [];
  let node = block, parent = null, lastDigit = null;
  if (node && typeof node === 'object' && typeof node._ === 'string') {
    chain.push(node._);
  }
  for (const d of digits) {
    if (!node || typeof node !== 'object' || !(d in node)) break;
    parent = node;
    lastDigit = d;
    node = node[d];
    if (typeof node === 'string') { chain.push(node); break; }
    if (node && typeof node === 'object' && typeof node._ === 'string') {
      chain.push(node._);
    }
  }
  return { chain, terminal: node, parent, lastDigit };
}

function bsp(block, number, point, mode) {
  // Dir (full)
  if (number == null && point == null && mode == null) {
    return { mode: 'dir', tree: block };
  }

  // Disc
  if (mode === 'disc' && point != null) {
    const target = typeof point === 'string' ? parseInt(point) : point;
    const nodes = [];
    (function collect(node, depth, path) {
      if (depth === target) {
        const text = typeof node === 'string' ? node : (node && node._ || null);
        nodes.push({ path, text });
        return;
      }
      if (!node || typeof node !== 'object') return;
      for (let d = 1; d <= 9; d++) {
        const k = String(d);
        if (k in node) collect(node[k], depth + 1, path ? `${path}.${k}` : k);
      }
    })(block, 0, '');
    return { mode: 'disc', depth: target, nodes };
  }

  const digits = parseAddress(number);
  const { chain, terminal, parent, lastDigit } = walk(block, digits);
  const fl = floorDepth(block);

  // Ring
  if (point === 'ring') {
    if (!parent || typeof parent !== 'object') return { mode: 'ring', siblings: [] };
    const siblings = [];
    for (let d = 0; d <= 9; d++) {
      const k = String(d);
      if (k === lastDigit || !(k in parent)) continue;
      const v = parent[k];
      const text = typeof v === 'string' ? v : (v && v._ || null);
      siblings.push({ digit: k, text, branch: typeof v === 'object' });
    }
    return { mode: 'ring', siblings };
  }

  // Dir (subtree)
  if (point === 'dir') {
    return { mode: 'dir', subtree: terminal };
  }

  // Point
  if (mode === 'point' && point != null) {
    const ps = typeof point === 'string' ? parseInt(point) : point;
    const idx = (fl - 1) - ps;
    if (idx >= 0 && idx < chain.length) return { mode: 'point', pscale: ps, text: chain[idx] };
    return { mode: 'point', pscale: ps, text: chain[chain.length - 1] || null };
  }

  // Spindle (default)
  return {
    mode: 'spindle',
    nodes: chain.map((text, i) => ({ pscale: (fl - 1) - i, text }))
  };
}

// Export for both Node and browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { bsp, floorDepth, parseAddress, walk };
}
