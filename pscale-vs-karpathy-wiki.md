# What Happens When You Add Coordinates to Karpathy's LLM Wiki

Karpathy's [LLM Knowledge Base](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) is a smart move: ditch vector databases, use Markdown files, let the LLM compile and maintain a wiki. It works because structure beats similarity search for mid-sized knowledge bases.

But it has a scaling wall. When your wiki grows past a few hundred pages, navigation degrades to search — and search is exactly the problem the wiki was meant to solve.

**Pscale** is what happens when you give every piece of knowledge a numeric address that encodes its own context.

## The Problem Karpathy Identifies (Correctly)

RAG is stateless. Every query re-discovers knowledge from scratch. Vector similarity misses conceptual connections. The context window resets between sessions.

His solution: an LLM-maintained Markdown wiki with backlinks. Raw sources stay immutable. The LLM compiles, summarises, and interlinks. Periodic linting keeps it healthy.

This is genuinely good. But three problems remain:

**1. Navigation is still search.** Backlinks help, but finding the right page in a 500-page wiki means grep, keyword matching, or an index file the LLM maintains. The wiki doesn't know its own structure — the LLM has to rediscover it each session.

**2. Compression is flat.** The wiki has two levels: raw sources and compiled summaries. There's no systematic relationship between compression levels. You can't ask "give me this topic at 3 different resolutions" because resolution isn't structural.

**3. Context assembly is manual.** When the LLM needs context for a task, it reads pages. Which pages? How much of each? The wiki can't answer this — the LLM guesses based on relevance, just like RAG but with better-structured documents.

## What Coordinates Change

A **pscale block** is a JSON document where position in the tree *is* the meaning. No metadata, no wrapper fields. Three conventions:

- `_` — content at the zero position (always a complete thought, never a heading)  
- `1`–`9` — branch positions (at most nine children per level)  
- `{}` — nesting depth encodes resolution scale

Here's a tiny example — a knowledge block about sorting algorithms:

```json
{
  "_": "Sorting algorithms trade time complexity against memory usage and stability. The choice depends on data characteristics and constraints.",
  "1": {
    "_": "Comparison-based sorts cannot beat O(n log n) average case.",
    "1": "Quicksort: O(n log n) average, O(n²) worst. In-place. Unstable. Cache-friendly. The practical default.",
    "2": "Mergesort: O(n log n) guaranteed. Requires O(n) extra space. Stable. Preferred when stability matters.",
    "3": "Heapsort: O(n log n) guaranteed. In-place. Unstable. Rarely fastest in practice due to cache behaviour."
  },
  "2": {
    "_": "Non-comparison sorts break the O(n log n) barrier by exploiting data structure.",
    "1": "Radix sort: O(nk) where k is key length. Requires fixed-width keys. Extraordinary for integers.",
    "2": "Counting sort: O(n+k) where k is range. Only works when range is bounded and small."
  }
}
```

Now the interesting part. A single function — **BSP** (Block Semantic Positioning) — navigates this:

```
bsp(block, 0.1)    → spindle: ["Sorting algorithms trade...", "Comparison-based sorts...", "Quicksort: O(n log n)..."]
bsp(block, 0.2)    → spindle: ["Sorting algorithms trade...", "Non-comparison sorts break..."]  
bsp(block, 0.12)   → spindle: ["Sorting algorithms trade...", "Comparison-based sorts...", "Mergesort: O(n log n)..."]
```

Each **spindle** returns a chain from broadest context to specific detail. You always get the full context — not just the leaf node, but every layer of meaning above it. The number `0.12` *is* the address, the context path, and the retrieval key simultaneously.

No search. No index file. No grep. The number tells you where to go and what context surrounds it.

## Logarithmic Compression (Where It Gets Interesting)

Karpathy's wiki compiles summaries. Pscale **compacts** — and the mechanic is precise:

Raw items fill positions 1 through 9. When the 10th arrives:
- A summary of items 1–9 goes to **position 10**
- The new raw item goes to **position 11**

Position 10 is pscale 1: what genuinely persisted across 9 items. Position 100 is pscale 2: a summary of summaries. Position 1000 is pscale 3.

**This is lossless.** The raw items remain. Summaries add resolution above the data, not instead of it.

The address `5432` means:
- **5** at pscale 3: the 5th summary-of-summary-of-summaries  
- **4** at pscale 2: the 4th summary-of-summaries within that range  
- **3** at pscale 1: the 3rd summary within that batch  
- **2** at pscale 0: the 2nd raw item in the current batch

To support item 5432 with context, pull `5000`, `5400`, `5430` — progressively wider lenses on the same stream. Or manoeuvre laterally: compare `1000`, `2000`, `3000`, `4000`, `5000` for the full arc.

**The numeric structure enables navigation without a search index.** Every pscale number implicitly contains its own context coordinates.

After 10,000 items, a Karpathy wiki needs 10,000+ pages plus an index. A pscale block has the same 10,000 items but also 1,111 summaries at four resolution levels, all addressable by number, all navigable in three BSP moves from anywhere.

## Context Assembly as Aperture

When an LLM needs context from a Karpathy wiki, it reads pages. How many? Which ones? That's a judgment call every session.

With pscale, context assembly is **aperture configuration**:

```
# Tight focus: just one topic at full depth
bsp(block, 0.312)  → 3-level spindle, ~100 tokens

# Wide survey: all top-level branches
bsp(block, _, 1, 'disc')  → all pscale 1 summaries, ~200 tokens

# Lateral scan: compare five arcs
bsp(block, 1000) + bsp(block, 2000) + bsp(block, 3000) ...  → trend view
```

The LLM doesn't search for relevant pages. It configures an aperture — how deep, how wide, from what origin — using numeric addresses. The block's structure IS the retrieval system.

## Multi-Agent Coordination (The Part Karpathy Can't Do)

Karpathy's wiki is single-player. One person, one LLM, one vault.

Pscale blocks enable something different: agents reading each other's structured state at known addresses. No message-passing. No coordination protocol. Each agent writes to its own block. Other agents read spindles from it.

```
Agent A's context window:
  - Own block spindle: ~150 tokens
  - Spindle from Agent B's block at known address: ~50 tokens  
  - Spindle from Agent C's block at known address: ~50 tokens
  Total: ~250 tokens for full mutual awareness
```

The coordination cost scales with spindle depth, not message count. Reading a 50-token spindle from another agent's block is incomparably cheaper than an agent-to-agent LLM call.

## Try It

BSP exists as a standalone function in [JavaScript](bsp.js) and [Python](bsp.py). Clone [the repo](https://github.com/pscale-commons/pscale), run:

```sh
# See the full structure
python3 bsp.py pscale-touchstone-lean

# Extract a spindle (broad → specific context chain)
python3 bsp.py pscale-touchstone-lean 0.1

# See what's at the same level as your current position
python3 bsp.py pscale-touchstone-lean 0.1 ring

# Slice across all branches at one depth
python3 bsp.py pscale-touchstone-lean _ 1 disc
```

The touchstone block is self-teaching — it describes BSP by being a BSP-navigable structure. Walk it to learn it.

## What This Is Not

This is not a replacement for Karpathy's wiki if you want a personal research tool you can set up in 20 minutes. His system is simpler and covers that use case well.

Pscale is for when you need:
- **Lossless history** at arbitrary scale (thousands of entries, navigable without search)
- **Structured context assembly** (aperture configuration, not page selection)
- **Multi-agent coordination** (shared state through structured reads)
- **Self-describing data** (the address IS the context)

If Karpathy's wiki is a library with a librarian, pscale is a coordinate system for knowledge — every piece of content knows where it is and what surrounds it.

## Links

- [BSP walker (JS + Python)](https://github.com/pscale-commons/pscale) — the navigation function
- [Pscale compaction reference](pscale-compaction-reference.md) — how logarithmic compression works
- [Touchstone](pscale-touchstone-lean.json) — self-teaching block: walk it to learn it

Created by [David Pinto](https://happyseaurchin.com). Built with Claude.
