#!/usr/bin/env python3
"""
bsp.py — pure-form BSP for pscale JSON blocks.

No tree wrapper, no tuning field, no metadata. The block IS the tree.
Floor derived from the underscore chain. Everything else is a walk.

Modes:
    bsp(block)                        → dir: full tree (depth-1 survey)
    bsp(block, number)                → spindle: root-to-target chain
    bsp(block, number, 'ring')        → ring: siblings at terminal
    bsp(block, number, 'dir')         → dir: subtree from target down
    bsp(block, number, pscale, 'point') → point: single node at pscale
    bsp(block, _, depth, 'disc')      → disc: all nodes at a depth

CLI:
    python tidy-up/bsp.py spark              # dir
    python tidy-up/bsp.py spark 0.21         # spindle
    python tidy-up/bsp.py spark 0.21 ring    # ring
    python tidy-up/bsp.py spark 0.21 dir     # subtree
    python tidy-up/bsp.py spark 0.3 -2 point # point at pscale -2
    python tidy-up/bsp.py spark _ 3 disc     # disc at depth 3
"""

import json, sys, os


def floor_depth(block):
    """Follow the underscore chain until a string. Count = floor."""
    node = block
    depth = 0
    while isinstance(node, dict) and '_' in node:
        depth += 1
        node = node['_']
        if isinstance(node, str):
            return depth
    return depth


def parse_address(number):
    """Parse a pscale number into a list of digit characters to walk.
    Leading 0 before decimal is notation (delineation marker), not a key."""
    s = f'{number:.10f}' if isinstance(number, (int, float)) else str(number)
    parts = s.split('.')
    integer = parts[0] or '0'
    frac = (parts[1] if len(parts) > 1 else '').rstrip('0')
    if integer == '0':
        return list(frac)
    return list(integer + frac)


def walk(block, digits):
    """Walk the tree collecting underscore texts. Returns (spindle, terminal_node, parent_node, terminal_digit)."""
    chain = []
    node = block
    parent = None
    last_digit = None

    # Collect root underscore
    if isinstance(node, dict) and isinstance(node.get('_'), str):
        chain.append(node['_'])

    for d in digits:
        if not isinstance(node, dict) or d not in node:
            break
        parent = node
        last_digit = d
        node = node[d]
        if isinstance(node, str):
            chain.append(node)
            break
        elif isinstance(node, dict) and isinstance(node.get('_'), str):
            chain.append(node['_'])

    return chain, node, parent, last_digit


def bsp(block, number=None, point=None, mode=None):
    """Pure-form BSP. Block is the tree — no wrapper."""

    # Dir (full) — no args
    if number is None and point is None and mode is None:
        return {'mode': 'dir', 'tree': block}

    # Disc — bsp(block, None, depth, 'disc')
    if mode == 'disc' and point is not None:
        target = int(point) if isinstance(point, str) else point
        nodes = []
        def collect(node, depth, path):
            if depth == target:
                text = node if isinstance(node, str) else (node.get('_') if isinstance(node, dict) else None)
                nodes.append({'path': path, 'text': text})
                return
            if not isinstance(node, dict):
                return
            for d in '123456789':
                if d in node:
                    collect(node[d], depth + 1, f'{path}.{d}' if path else d)
        collect(block, 0, '')
        return {'mode': 'disc', 'depth': target, 'nodes': nodes}

    # Parse address and walk
    digits = parse_address(number)
    chain, terminal, parent, last_digit = walk(block, digits)
    fl = floor_depth(block)

    # Ring — siblings at terminal
    if point == 'ring':
        if parent is None or not isinstance(parent, dict):
            return {'mode': 'ring', 'siblings': []}
        siblings = []
        for d in '0123456789':
            if d == last_digit or d not in parent:
                continue
            v = parent[d]
            text = v if isinstance(v, str) else (v.get('_') if isinstance(v, dict) else None)
            siblings.append({'digit': d, 'text': text, 'branch': isinstance(v, dict)})
        return {'mode': 'ring', 'siblings': siblings}

    # Dir (subtree)
    if point == 'dir':
        return {'mode': 'dir', 'subtree': terminal}

    # Point — content at a specific pscale
    if mode == 'point' and point is not None:
        ps = int(point) if isinstance(point, str) else point
        # pscale = (floor - 1) - index, where index 0 is root
        target_index = (fl - 1) - ps
        if 0 <= target_index < len(chain):
            return {'mode': 'point', 'pscale': ps, 'text': chain[target_index]}
        return {'mode': 'point', 'pscale': ps, 'text': chain[-1] if chain else None}

    # Spindle (default) — annotate with pscale
    nodes = []
    for i, text in enumerate(chain):
        nodes.append({'pscale': (fl - 1) - i, 'text': text})
    return {'mode': 'spindle', 'nodes': nodes}


# ---- CLI ----

def fmt_spindle(r):
    return '\n'.join(f"  [{n['pscale']:>3}] {n['text'][:200]}{'...' if len(n['text']) > 200 else ''}" for n in r['nodes'])

def fmt_ring(r):
    if not r.get('siblings'):
        return '  (no siblings)'
    return '\n'.join(f"  {s['digit']}: {(s.get('text') or '(branch)')[:120]}{'...' if len(s.get('text','')) > 120 else ''}{' +' if s.get('branch') else ''}" for s in r['siblings'])

def fmt_disc(r):
    if not r.get('nodes'):
        return '  (no nodes at this depth)'
    return '\n'.join(f"  [{n['path']}] {(n.get('text') or '(no text)')[:150]}" for n in r['nodes'])

def fmt_dir(r):
    tree = r.get('subtree') or r.get('tree', {})
    if 'subtree' in r:
        return json.dumps(tree, indent=2, ensure_ascii=False)
    lines = []
    root = tree.get('_', '')
    if root:
        lines.append(f"  _: {root[:200]}{'...' if len(root) > 200 else ''}")
    for k in sorted(k for k in tree if k != '_'):
        v = tree[k]
        text = v if isinstance(v, str) else (v.get('_', '(branch)') if isinstance(v, dict) else str(v))
        lines.append(f"  {k}: {text[:120]}{'...' if len(text) > 120 else ''}")
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tidy-up/bsp.py <block> [number|_] [ring|dir|pscale] [point|disc]")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    block_name = sys.argv[1]
    path = os.path.join(script_dir, f'{block_name}.json')
    if not os.path.exists(path):
        print(f"Block not found: {path}")
        sys.exit(1)
    with open(path) as f:
        block = json.load(f)

    args = sys.argv[2:]
    number = None
    point = None
    mode = None

    if args:
        if args[0] == '_':
            number = None
        else:
            try:
                number = float(args[0])
            except ValueError:
                print(f"Invalid number: {args[0]}")
                sys.exit(1)

    if len(args) > 1:
        a = args[1]
        if a in ('ring', 'dir'):
            point = a
        elif a == 'disc':
            mode = 'disc'
        else:
            try:
                point = int(a)
            except ValueError:
                point = a

    if len(args) > 2:
        a = args[2]
        if a in ('point', 'disc'):
            mode = a

    result = bsp(block, number, point, mode)
    m = result.get('mode')

    if m == 'spindle':
        print(f"[{block_name} {number}] spindle")
        print(fmt_spindle(result))
    elif m == 'ring':
        print(f"[{block_name} {number} ring]")
        print(fmt_ring(result))
    elif m == 'dir':
        label = f"{block_name} {number} dir" if number else f"{block_name} dir"
        print(f"[{label}]")
        print(fmt_dir(result))
    elif m == 'point':
        print(f"[{block_name} {number} point @ pscale {result.get('pscale')}]")
        print(f"  {result.get('text')}")
    elif m == 'disc':
        print(f"[{block_name} disc @ depth {result.get('depth')}]")
        print(fmt_disc(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
