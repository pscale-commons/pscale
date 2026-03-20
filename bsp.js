/**
 * bsp.js — pure-form BSP for pscale JSON blocks.
 *
 * No tree wrapper, no tuning field, no metadata. The block IS the tree.
 * Floor derived from the underscore chain. Digit 0 maps to key '_'.
 *
 * Address conventions:
 *   0.x     Delineation (floor 1). Leading 0 is notation, not a key.
 *   100     Accumulation (floor 3). Digit 1 at top level, zeros = no branch taken.
 *   001.1   Floor 3. Two zeros walk underscore chain to floor, then digits below.
 *   Digit 0 always maps to key '_' — walking the underscore spine.
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
  let node = block, parent = null, lastKey = null, depth = 0;

  // Collect root text: follow underscore chain to the floor string.
  // Floor 1: root._ is the string directly.
  // Floor N: root._._._ ... N deep to hit the string.
  if (node && typeof node === 'object' && '_' in node) {
    let inner = node._;
    while (inner && typeof inner === 'object' && '_' in inner) inner = inner._;
    if (typeof inner === 'string') chain.push({ text: inner, depth });
  }

  for (const d of digits) {
    const key = d === '0' ? '_' : d;
    if (!node || typeof node !== 'object' || !(key in node)) break;
    const target = node[key];
    // Walking '0' into a string '_' means we've hit the floor spine —
    // this text was already collected when we arrived at this node.
    if (d === '0' && typeof target === 'string') break;
    parent = node;
    lastKey = key;
    node = target;
    depth++;
    if (typeof node === 'string') {
      chain.push({ text: node, depth });
      break;
    }
    if (node && typeof node === 'object' && typeof node._ === 'string') {
      chain.push({ text: node._, depth });
    }
  }

  return { chain, terminal: node, parent, lastKey };
}

function bsp(block, number, point, mode) {
  const fl = floorDepth(block);

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
        let text;
        if (typeof node === 'string') { text = node; }
        else if (node && typeof node === 'object') {
          let inner = node._;
          while (inner && typeof inner === 'object' && '_' in inner) inner = inner._;
          text = typeof inner === 'string' ? inner : null;
        } else { text = null; }
        nodes.push({ path, text });
        return;
      }
      if (!node || typeof node !== 'object') return;
      // Walk underscore child (digit 0)
      if ('_' in node && typeof node._ === 'object') {
        collect(node._, depth + 1, path ? `${path}.0` : '0');
      }
      for (let d = 1; d <= 9; d++) {
        const k = String(d);
        if (k in node) collect(node[k], depth + 1, path ? `${path}.${k}` : k);
      }
    })(block, 0, '');
    return { mode: 'disc', depth: target, nodes };
  }

  const digits = parseAddress(number);
  const { chain, terminal, parent, lastKey } = walk(block, digits);

  function pscaleAt(depth) {
    return (fl - 1) - depth;
  }

  // Ring
  if (point === 'ring') {
    if (!parent || typeof parent !== 'object') return { mode: 'ring', siblings: [] };
    const siblings = [];
    // Include '_' as navigable sibling (digit 0) if it's an object
    if (lastKey !== '_' && '_' in parent && typeof parent._ === 'object') {
      let inner = parent._;
      let text = null;
      while (inner && typeof inner === 'object' && '_' in inner && typeof inner._ === 'object') {
        inner = inner._;
      }
      if (inner && typeof inner === 'object' && typeof inner._ === 'string') {
        text = inner._;
      }
      siblings.push({ digit: '0', text, branch: true });
    }
    for (let d = 1; d <= 9; d++) {
      const k = String(d);
      if (k === lastKey || !(k in parent)) continue;
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
    for (const entry of chain) {
      if (pscaleAt(entry.depth) === ps) {
        return { mode: 'point', pscale: ps, text: entry.text };
      }
    }
    const last = chain[chain.length - 1];
    return { mode: 'point', pscale: ps, text: last ? last.text : null };
  }

  // Spindle (default)
  return {
    mode: 'spindle',
    nodes: chain.map(entry => ({ pscale: pscaleAt(entry.depth), text: entry.text }))
  };
}

// Export for both Node and browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { bsp, floorDepth, parseAddress, walk };
}
