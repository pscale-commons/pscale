# pscale

A semantic number system for structured knowledge. Pscale blocks are JSON documents where position in the tree *is* the data — depth encodes resolution, branch position encodes relationship, and a single navigation function (BSP) can extract any view from any block.

## Documents

Three companion blocks, each teaching a different aspect:

- **pscale-touchstone.json** — The format specification. A pscale block that teaches pscale by being an operational example of itself. Start here.
- **pscale-touchstone-lean.json** — Lean version of the touchstone.
- **pscale-guidelines.json** / **pscale-guidelines.md** — Block authoring craft. How to write pscale blocks that produce rich, useful spindles.
- **pscale-design.json** / **pscale-design.md** — Systems design wisdom for building on pscale, where LLMs inhabit and navigate their own semantic space.

## BSP (Block Semantic Positioning)

BSP is the navigation function. Two implementations are provided:

```sh
# Python
python3 bsp.py pscale-touchstone 0.21          # spindle: root → section 2 → subsection 1
python3 bsp.py pscale-touchstone               # dir: full tree overview
python3 bsp.py pscale-touchstone 2.1 ring      # ring: siblings at terminal
python3 bsp.py pscale-touchstone _ 3 disc      # disc: all nodes at depth 3

# JavaScript
node bsp.js pscale-touchstone 0.21
node bsp.js pscale-touchstone
```

## Format

Three JSON conventions, nothing else:

- `_` — meaning at the zero position (always a complete thought, never a heading)
- `1`–`9` — branch positions (at most nine children per level)
- `{}` — nesting depth encodes resolution scale

No metadata, no wrapper fields. The structure is the complete specification.

## Related repos

- [pscale-commons/agents](https://github.com/pscale-commons/agents) — LLM agents running on pscale
- [pscale-commons/seed-spore](https://github.com/pscale-commons/seed-spore) — the pscale seed and its teaching companion

## Author

Created by [David Pinto](https://hermitcrab.me).

## License

[MIT](LICENSE)
