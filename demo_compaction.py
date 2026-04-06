#!/usr/bin/env python3
"""
demo_compaction.py — See pscale BSP navigation in action.

Loads the real pscale-touchstone-lean block and demonstrates spindle,
ring, and disc navigation — showing how numeric addresses replace search.

Usage (run from the pscale-commons/pscale repo directory):
    python3 demo_compaction.py

Or point it at the touchstone-lean block:
    python3 demo_compaction.py /path/to/pscale-touchstone-lean.json
"""

import json, sys, os

# ─── Import the real BSP function ───
# Expects bsp.py in the same directory (as in pscale-commons/pscale repo)

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from bsp import bsp


def load_block(path=None):
    """Load the touchstone-lean block."""
    if path is None:
        path = os.path.join(script_dir, 'pscale-touchstone-lean.json')
    if not os.path.exists(path):
        print(f"Block not found: {path}")
        print("Run this from the pscale-commons/pscale repo directory,")
        print("or pass the path to pscale-touchstone-lean.json as an argument.")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def fmt_spindle(result):
    """Format a spindle result for display."""
    lines = []
    for n in result['nodes']:
        text = n['text'][:100] + ('...' if len(n['text']) > 100 else '')
        lines.append(f"    [pscale {n['pscale']:>3}] {text}")
    return '\n'.join(lines)


def fmt_ring(result):
    """Format a ring result for display."""
    lines = []
    for s in result['siblings']:
        text = (s.get('text') or '(branch)')[:100]
        marker = ' +' if s.get('branch') else ''
        lines.append(f"    {s['digit']}: {text}{marker}")
    return '\n'.join(lines)


def fmt_disc(result):
    """Format a disc result for display."""
    lines = []
    for n in result['nodes']:
        text = (n.get('text') or '(no text)')[:100]
        lines.append(f"    [{n['path']}] {text}")
    return '\n'.join(lines)


# ─── Run the demo ───

block_path = sys.argv[1] if len(sys.argv) > 1 else None
block = load_block(block_path)

print("=" * 70)
print("PSCALE BSP DEMO — Real navigation on pscale-touchstone-lean")
print("=" * 70)
print()

# 1. Orientation: bare dir
print("─── 1. What is this block? (dir) ───")
print()
result = bsp(block)
tree = result['tree']
root_text = tree.get('_', '')
if isinstance(root_text, str):
    print(f"  Root: {root_text[:120]}...")
print(f"  Branches: {', '.join(k for k in sorted(tree.keys()) if k != '_')}")
print()

# 2. Spindle: walk into branch 1
print("─── 2. Spindle: bsp(block, 1) — walk into branch 1 ───")
print()
result = bsp(block, 1)
print(fmt_spindle(result))
print()

# 3. Deeper spindle: walk into branch 1, child 1
print("─── 3. Deeper spindle: bsp(block, 1.1) — branch 1, child 1 ───")
print()
result = bsp(block, 1.1)
print(fmt_spindle(result))
print()

# 4. Even deeper: branch 1, child 1, grandchild 2
print("─── 4. Deep spindle: bsp(block, 1.12) — three levels deep ───")
print()
result = bsp(block, 1.12)
print(fmt_spindle(result))
print()

# 5. Ring: what else is at the same level as branch 1?
print("─── 5. Ring: bsp(block, 1, 'ring') — siblings of branch 1 ───")
print()
result = bsp(block, 1, 'ring')
print(fmt_ring(result))
print()

# 6. Disc: slice across all branches at depth 1
print("─── 6. Disc: bsp(block, None, 1, 'disc') — all nodes at depth 1 ───")
print()
result = bsp(block, None, 1, 'disc')
print(fmt_disc(result))
print()

# 7. The contrast
print("─── What Karpathy's wiki gives you ───")
print()
print("  Markdown pages + index file.")
print("  To find content: grep, keyword matching, or LLM search.")
print("  To get context: read surrounding pages.")
print("  To get overview: read the whole index.")
print()

print("─── What pscale gives you ───")
print()
print("  One JSON block. Numeric addresses. No search.")
print("  bsp(block, 1)    → spindle: root context + branch 1 summary")
print("  bsp(block, 1.12) → spindle: root + branch 1 + child 1 + leaf 2")
print("  bsp(block, 1, 'ring') → what else exists alongside branch 1")
print("  bsp(block, _, 1, 'disc') → all summaries at the same depth")
print()
print("  The number IS the retrieval key. The spindle IS the context.")
print("  Every address includes its own context chain — structural, not optional.")
print()

print("─── Try it yourself ───")
print()
print("  git clone https://github.com/pscale-commons/pscale")
print("  cd pscale")
print("  python3 bsp.py pscale-touchstone-lean 0.1")
print()
print("  The touchstone block teaches BSP by being a BSP-navigable structure.")
print("  Walk it to learn it.")
print()
