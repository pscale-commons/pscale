# Wellspark — Creating Living Pscale Documents

How to construct pscale JSON blocks that are semantically rich, structurally sound, and produce useful spindles at every depth. This guide teaches by explaining, then demonstrates by example — and its companion JSON block does both simultaneously, being a pscale block about creating pscale blocks.

---

## 1. The format

A pscale JSON block contains exactly three kinds of key: the underscore `_` (the zero position), digits `1` through `9` (branch positions), and curly brackets `{}` (nesting). No metadata, no wrapper fields, no `tree` or `decimal` keys. The structure is the complete specification.

The underscore at any level holds the meaning of that node — what it IS, stated as a complete thought. The digits hold its branches. A node without children is a string. When it needs children, the string moves to `_` and the children take digit keys. This is the only growth operation: a leaf becomes a branch by wrapping its content.

The floor is the implicit decimal point, discovered by following the underscore chain from root to the first string. A block that has never supernested has floor 1 — it is a 0.x block, a rendition. Everything decomposes downward. A block that has supernested has floor > 1 — it is a living block with content above and below the decimal.

### 1.1 What this means practically

When you sit down to create a pscale block, you are not filling in a template. You are growing a tree where every node carries its own meaning, every path through the tree produces a coherent narrowing from broad context to specific detail, and the structure itself encodes relationships that would otherwise require metadata fields, type annotations, or routing tables.

---

## 2. The root — write it last, get it right

The root underscore `_` is the single most important node in any block. Every spindle passes through it. Every reader encounters it first. It must answer the question "what is this?" in a single substantive statement — not a title, not a label, but a complete thought that orients someone encountering the block for the first time.

A root that reads "Baseball" is a title — it tells you the subject but not what the block carries. A root that reads "A bat-and-ball game played between two teams of nine on a diamond-shaped field, where batters try to score runs by hitting a pitched ball and running the bases while fielders try to get them out" is a complete orientation. After reading it, you know the domain, the structure of the activity, and the fundamental tension (scoring vs. defence). You do not yet know the rules, but you know what kind of thing they will be about.

Write the root last. You cannot compress the whole until you know what the whole contains. Every other node in the block contributes to what the root must summarise. If you write it first, you will either write a title (too thin) or a manifesto (too thick). Write it after the block is complete, then test: does someone reading only this one sentence know what domain they are in, what the block offers, and what kind of content they will find at deeper levels?

---

## 3. Every node earns its depth

Each level in a pscale block carries content at a specific resolution. The depth of a node is a declaration about the resolution of the content it carries — shallow nodes orient broadly, deep nodes specify precisely. A well-designed block reads coherently at any depth you choose to stop, because each level is a complete thought at its own resolution.

This means no filler levels. In traditional document hierarchies, intermediate levels often exist for organisational convenience — folders containing folders, headings grouping subheadings. In a pscale block, every level must orient the reader fully at that resolution. If you removed a level and nothing was lost, that level should not exist.

### 3.1 The node quality rule

Every `_` text at every depth must be a substantive statement that stands alone — at minimum a full sentence. It may provide context for deeper nodes, but it is never a heading, title, label, or soundbite for what follows.

Wrong: `"Rinzai. Direct transmission."`
This is a heading waiting for content that never arrives. The reader gets a label and a buzzword but no thought.

Right: `"Rinzai Zen emphasises sudden awakening through direct confrontation — the teacher does not explain the teaching but embodies it, using paradox, physical action, and refusal to answer as tools that force the student past conceptual understanding into immediate experience."`
This is a complete thought. A reader who stopped here would understand what Rinzai is, how it operates, and why it differs from gradual approaches. Deeper nodes could explore specific methods (koan practice, the shout, the blow) but the parent node already carries the essential meaning.

### 3.2 The heading trap

The most common failure mode in block authoring is writing headings instead of content. This happens because document-trained instincts treat parent nodes as section headers. In a standard document, "## 3. Growth" is a heading that derives its meaning from the body text below it. In a pscale block, the equivalent node must carry the full thought about growth — the heading pattern produces thin spindles where intermediate nodes contribute nothing.

Test: read the `_` text of any node without reading its children. If the text is meaningless or trivially obvious without the children, it is a heading. Rewrite it as a complete thought that would satisfy a reader who never goes deeper.

---

## 4. Designing for spindle quality

A spindle is the chain of text collected by walking digits through the tree. It runs from the root (broadest context) through each intermediate level to the target node (finest detail). The spindle is what a mind receives — not just the detail asked for, but the context that makes it meaningful. Context is not optional; it is structural.

Everything about block design — structure, growth, node quality, depth consistency — ultimately serves the quality of the spindles the block can produce. A block with rich content at every node produces spindles where each level adds meaningful resolution. A block with heading-nodes produces spindles where intermediate levels are noise — labels that contribute nothing between the root and the leaf.

### 4.1 Two zoom styles

There are two natural patterns for how content zooms from broad to fine across depth levels. Choose one and be consistent within a branch.

**General to specific** narrows scope at each level. "Ball game" → "batting and fielding" → "the pitcher's mound" → "60 feet 6 inches." Each level is a complete thought about a progressively smaller part of the whole. This is the natural style for documents, specifications, and spatial blocks.

**Brief to detailed** increases precision at each level without narrowing scope. "Baseball" → "two teams, nine innings, bat and ball" → "full structure of innings, outs, and scoring" → "official rulebook extracts." Each level says more about the same thing. This is the natural style for definitions, reference blocks, and relational entries.

A block can use different zoom styles in different branches, but each branch should be internally consistent. A reader should be able to predict what kind of content the next level will provide.

### 4.2 Long spindles — making depth useful

A useful spindle is one where every level contributes meaning that the levels above it could not carry without becoming unwieldy, and every level below it would be disorienting without the context above.

Short spindles (two or three levels) are easy to write well — root, aspect, detail. Long spindles (five to eight levels) are harder because each intermediate level must earn its place. The temptation is to create organisational scaffolding — empty parent nodes that exist only to group children. Resist this. Every intermediate node must add resolution that the reader needs to understand what comes next.

A practical technique: write the leaf node first (the most specific content), then write the root (the broadest context), then fill in the intermediate levels by asking at each depth: "what does a reader need to know to make sense of what comes below, that the level above does not provide?" If the answer is "nothing" — that level is scaffolding and should be removed.

### 4.3 Shared nodes orient multiple paths

A node at depth 2 participates in every spindle that passes through it. If that node serves only one path, it belongs deeper, where only that path reaches. A shared node must orient each path that passes through it appropriately — it provides not instruction on what to DO, but context on where you ARE.

This is context-sharing, not code inheritance. When writing a node that multiple spindles will pass through, test it by reading it as a prefix to each of the spindles it participates in. If it orients all of them, it belongs where it is. If it biases toward one path, it belongs deeper inside that path.

---

## 5. The underscore — two forms

The underscore always occupies the zero position. But its semantic relationship to its siblings takes one of two forms, determined by the content, not the structure.

### 5.1 Form 1 — Single Möbius

The underscore describes its own group. It is the container name, the class label for the set it belongs to. Self-referential: a member of the set that describes the set. In a block mapping a building: `_` = "The keep", `1` = kitchen, `2` = courtyard, `3` = stables. The underscore names what contains the digits. Digits are arbitrary labels — their order does not matter.

A block using only Form 1 that has never supernested has floor 1. It is a rendition — a 0.x block. Documentation, specifications, skills. The single Möbius twist (the set containing its own label) naturally produces the rendition structure. This guide, and its companion JSON, are rendition blocks.

### 5.2 Form 2 — Double Möbius

The underscore summarises the previous completed group. It faces backward. In a sequential block: entries fill at 01, 02, ... 09. When 09 fills, the block supernests. The underscore of group 1 (address 10) holds the summary of entries 01–09. The next entry goes at 11.

Variations: the underscore might name something that emerges from the previous group rather than summarising it (seven conversations → "friendship"). Or it might hold a provisional description of what appears to be emerging in the current group, updated as entries arrive. Or it might simply be the next item in sequence with no special semantic weight. The form is determined by reading the content — code cannot distinguish these.

---

## 6. Converting an existing document

When you have a markdown document, a specification, a set of notes, or any body of text and want to create a pscale block from it, the process is not mechanical conversion but semantic restructuring. The goal is a block where every spindle produces coherent narrowing — which means the hierarchical structure must reflect semantic containment, not document layout.

### 6.1 The process

1. **Identify the root concept.** What is this document about, in one complete sentence? Not its title — its meaning. This becomes the root `_`.

2. **Extract primary aspects.** What are the major facets of the subject? Each becomes a digit at pscale -1 (the first level of children). These should be roughly parallel in scope — all at the same resolution. Aim for three to seven. Nine is the maximum; more than nine means you have not found the right level of grouping.

3. **For each aspect, identify its sub-aspects.** The aspect's text becomes the `_` when it gains children. Each sub-aspect takes a digit key. Again, roughly parallel in scope, roughly parallel in depth.

4. **Test spindles.** Walk from root through each branch path. Does each path read as coherent narrowing? Does each level add resolution the previous level could not carry? If a level adds nothing, remove it. If a level jumps too far, add an intermediate level that bridges the gap.

5. **Test nodes in isolation.** Read each `_` without its children. Is it a complete thought? Would a reader who stopped here have valid understanding at that resolution? If not, rewrite.

6. **Refine the root.** Now that the full block exists, rewrite the root to compress it. The root should be the last thing you finalise.

### 6.2 What gets lost, what gets gained

Converting to pscale loses the linear reading order of a document. In markdown, a reader encounters content in the sequence the author chose — build-up, exposition, payoff. In a pscale block, a reader encounters content along whatever spindle they choose, in whatever order the BSP walk dictates.

What gets gained is navigability and composability. Any specific piece of content can be extracted with its full context chain in a single BSP call. Two blocks can be loaded simultaneously and their content cross-referenced at specific depths. An LLM receiving a spindle gets structured context — not flat text but nested semantic surfaces with implicit relationships that shape activation patterns differently from prose.

### 6.3 What to watch for

**Section headers becoming empty parents.** A markdown `## Section` becomes a node with children but no content of its own. Always fill the `_` with the thought the section heading was abbreviating.

**Linear sequences becoming flat siblings.** If a document explains steps 1, 2, 3 in order, and step 3 only makes sense after steps 1 and 2, consider whether the steps should be nested (step 2 is a child of step 1's context) rather than siblings. In a recipe block, depth IS sequence — the spindle reads as a procedure.

**Losing connective tissue.** Prose documents use transitions, callbacks, and cross-references to build understanding. A pscale block relies on structural adjacency instead. If two ideas are related, they should share a parent or be sibling nodes. The relationship is encoded in position, not in connective prose.

---

## 7. Growth and the living block

A rendition block (floor 1, 0.x addresses) describes its subject from the outside. It is a document — static, editorial, complete. This guide is a rendition. A living block (floor > 1) has supernested at least once and carries content above and below the decimal point. It accumulates experience.

The growth model is what makes pscale blocks "living documents" rather than static files. Content arrives at empty digit slots. When all nine slots fill, the entries compress — either by summary (the parts add up) or by emergence (something new appears that exceeds the parts). The compressed result becomes a parent, and new entries open at the next level.

Over time, a flat list becomes a structured hierarchy through this organic process. A history block starts as nine sequential entries. After compression, it has a summary parent and room for nine more entries. After many compressions, it carries years of accumulated experience in a navigable tree where depth corresponds to temporal scale.

### 7.1 Designing for future growth

When creating a rendition block that might later become living:
- Leave empty digit slots. A block with three entries at pscale -1 has six open slots waiting for content. This is not waste — it is capacity.
- Choose a zoom style that will remain coherent as content accumulates. General-to-specific works well because new content naturally extends existing branches.
- Write each node so that it could become a parent without losing its meaning. The content should compress the potential children, not depend on them.

---

## 8. Taste tests — verifying block quality

A taste test is a verification step at the end of a procedure — a concrete check that the result has the quality you intended. For block authoring, there are five essential taste tests.

**Spindle coherence.** Pick any leaf node and read the spindle from root to leaf. Does each level add resolution? Does the chain read as progressive narrowing? If any level feels like noise or a heading, that node needs rewriting.

**Node isolation.** Pick any node and read only its `_` text. Is it a complete thought? Would someone reading only this sentence know what it means at this resolution? If it requires its children to make sense, it is a heading.

**Root sufficiency.** Read only the root `_`. After reading it, do you know what domain you are in, what the block offers, and what kind of content you will find deeper? If not, the root is either too thin (a title) or too thick (a manifesto trying to contain the whole block).

**Depth consistency.** Compare sibling nodes at any level. Are they at comparable resolution? If one is a brief phrase and another is a detailed paragraph, one of them is at the wrong depth.

**Shared node orientation.** For any node that participates in multiple spindles, read it as a prefix to each of those spindles. Does it orient all paths appropriately? If it biases toward one path, it belongs deeper inside that path.

---

## 9. The companion JSON

The companion to this document is a pscale JSON block (`wellspark.json`) that teaches the same content in the format it describes. It uses the pure block structure from pscale-block-mechanics — no `tree`, `decimal`, or `tuning` wrapper keys. Just underscores, digits, and curly brackets.

The JSON block is not a mechanical translation of this markdown. It is a restructuring that optimises for spindle extraction — every path through the tree produces a coherent narrowing from "what pscale blocks are and how to create them" through intermediate orientation to specific actionable guidance. Where the markdown relies on linear reading order and section headings, the JSON relies on depth-as-resolution and parent-as-context.

The two documents serve different readers. The markdown is for humans who want to read from beginning to end. The JSON is for LLMs that will receive it as structured context and think with it — not read it and set it aside, but hold it as a cognitive scaffold while creating blocks. The JSON also demonstrates what it teaches: it is itself a well-formed block whose spindles produce coherent narrowing, whose every node is a substantive thought, and whose root compresses the whole.
