# pscale

A semantic number system for structured knowledge. Pscale blocks are JSON documents where position in the tree *is* the data — depth encodes resolution, branch position encodes relationship, and a single navigation function (BSP) can extract any view from any block.

## Documents

- **pscale-touchstone.json** — The irreducible format specification. A pscale block that teaches pscale by being an operational example of itself. Start here.
- **pscale-guidelines.json** / **pscale-guidelines.md** — Block authoring craft. How to write pscale blocks that work.
- **pscale-design.json** / **pscale-design.md** — Systems design wisdom for building on pscale.

## BSP (Block Semantic Positioning)

BSP is the navigation function. Two implementations are provided:

```sh
# Python
python3 bsp.py pscale-touchstone 0.21          # spindle: root → section 2 → subsection 1
python3 bsp.py pscale-touchstone               # dir: full tree overview

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

## Author

Created by [David Pinto](https://hermitcrab.me).

## License

[MIT](LICENSE)
