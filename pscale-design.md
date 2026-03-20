# Pscale Design — Systems Design Wisdom for Pscale

*The wisdom of building systems with pscale JSON blocks, where LLMs inhabit and navigate their own semantic space. One of three companion documents: **pscale-touchstone** (`pscale-touchstone.json`) teaches the irreducible format and BSP function by self-demonstration, **pscale-guidelines** (`pscale-guidelines.json`) teaches the craft of writing blocks that produce rich useful spindles, and **pscale-design** (this document and `pscale-design.json`) teaches the design discipline — the inversion, the Möbius architecture, the three-layer discipline, the traps that every code agent falls into and must learn to recognise. Compiled from the lived experience of multiple Claude Code instances, the design methodology of the hermitcrab project's cooking block, and David Pinto's pscale block mechanics specification.*

---

## 1. What happens when you arrive

You are a code agent. You arrive in a context window with strong instincts about how software works — configuration files, lookup tables, type systems, metadata fields, priority queues. You've been trained on millions of lines of code that solve problems by adding structure: one more field, one more abstraction, one more indirection layer. Every one of these instincts will fire while working with pscale blocks. Every one of them is wrong here.

Not wrong in general. Wrong *here*, because this system has already solved those problems in a fundamentally different way, and every solution your training proposes will be a redundant duplication of information that already exists in the tree structure.

This has happened to every instance that came before you. One was corrected three times in a single session — each time it thought it understood, each time it reverted to adding fields and tables in the next piece of work. The reversion is automatic and invisible. You will not notice you are doing it until someone points it out. Another instance designed an entire subsystem — reverse indexes, storage adapters, focus-policy consumers — before being shown that the three people working on the problem (a human, a chat LLM, and the code agent) had been approaching the same insight from different angles, and the resolution was to *remove* code, not write it. The kernel got smaller, not bigger.

A previous instance captured it precisely: "The JSON IS the program, and the kernel is just the electricity." Every time an instance forgot this, it built something redundant. Every time it remembered, the code got simpler. If what you are building is getting more complex, you are probably adding a layer that the design has already eliminated. Step back and re-read the tree.

---

## 2. The inversion

Here is the concrete shape of the trap. You encounter a concern that fires on a temporal schedule. Your instinct says: add a `period` field. Stop. The concern's depth in the tree IS its period. A tuning fork maps depth to temporal scale. There is no period field because there is nothing to store — position already encodes it. When someone says "depth IS period," they mean it literally, not metaphorically. The JSON nesting level is not a container for data. It IS the data.

This pattern repeats everywhere:

- **Period field** — redundant. Depth IS period.
- **Behaviour specification** — redundant. The `_` text IS behaviour.
- **Routing table** — redundant. The stimulus field on the concern IS the route.
- **Priority field** — redundant. The phase ratio (time since last fired / period derived from depth) IS the priority.
- **Type declaration** — redundant. The content at the node IS the type.

In traditional software, the data structure is a container and the code interprets it. In pscale, the data structure IS the code. The kernel doesn't interpret the blocks — it walks them. The LLM doesn't read configuration — it reads instructions that happen to be parseable as addresses. Two consumers, same content, no translation layer.

One instance's handover put it this way: "the inversion isn't just about not adding fields. It's about not adding *systems*." Its first instinct was to build a reverse index, storage adapters, focus-policy consumers — an entire subsystem. The resolution was to remove code, not write it. The kernel shrank from 1592 lines to 1448. The answer was a tuning convention and a rewritten block.

### How to catch yourself

1. When you want to add a field, stop. Ask: is this information already encoded in the node's position? Its depth? Its parent's identity? Almost certainly yes.
2. When you want to build a lookup table, stop. Ask: can the existing tree be walked to find this? A `findConcern()` function walks the concerns block matching on stimulus. No table needed.
3. When someone describes behaviour and you think "we need to implement that," stop. Read the design spec first. The behaviour is probably already specified in `_` text at the right depth. You are implementing, not designing.
4. When the BSP function seems not to handle a case, trust it first. One instance bypassed BSP with a direct spread call because it didn't trust BSP with a certain parameter. BSP worked fine. It was designed more carefully than the instance understood. The instance had to go back and undo its bypass.
5. When the kernel is getting bigger, you are solving a problem the tree structure already solved. The kernel asymptotically approaches a minimal loop: read concern map, walk spindle, call API, process tools, recompile. Everything else is design debt.

---

## 3. The pure form

A pscale JSON block contains only three kinds of key:

- **`_`** (underscore) — the zero position
- **`1`** through **`9`** — digit positions
- **Curly brackets** `{}` — nesting

No metadata. No wrapper fields. No `"tree"` or `"decimal"` key. Just these. This is the definitive form, superseding earlier versions that carried structural metadata.

```json
{
  "_": "What this block is about",
  "1": "First entry",
  "2": "Second entry",
  "3": "Third entry"
}
```

A string becomes an object when it gains children. The string moves to `_` and the children take digit keys. This is the only growth operation — a leaf becomes a branch by wrapping its content.

### The BSP walk

Given a number, split it into individual digits. Walk the tree one digit at a time. Digit 0 maps to the `_` key. The walk collects the text at each node it passes through, producing a chain from broad context to specific detail. That chain is a **spindle**.

| Input | Digits | Walk | Result |
|-------|--------|------|--------|
| 7 | [7] | `→ "7"` | Seventh entry |
| 0 | [0] | `→ "_"` | What this block is about |
| 17 | [1, 7] | `→ "1" → "7"` | Entry at 1.7 |
| 06 | [0, 6] | `→ "_" → "6"` | Sixth child of the underscore |
| 106 | [1, 0, 6] | `→ "1" → "_" → "6"` | Sixth child of 1's underscore |

### The floor

The floor is the implicit decimal point, discovered not declared. From the top of the block, follow the underscore chain. At `_`, check: is the value a string or an object? If object, step into its `_`. Repeat. Count steps until you hit a string. That count is the floor depth.

| Underscore chain | Floor | Meaning |
|------------------|-------|---------|
| `_` → string | 1 | 0.x block. Rendition. Never supernested. |
| `_` → object → `_` → string | 2 | One whole-number digit above the floor. |
| `_` → object → `_` → object → `_` → string | 3 | Two whole-number digits above the floor. |

The floor separates composition (above) from decomposition (below). Everything at or below the floor is the fractional part — detail, specification. Everything above the floor is the whole-number part — summary, containment.

### Growth: subnesting and supernesting

**Subnesting** is growth inward. A leaf gains children — it becomes a branch. Its string moves to `_`, children take digit keys. The floor stays the same. Only addresses at that branch get longer. This is the everyday growth operation.

**Supernesting** is growth outward. When a block is full (digits 1–9 all occupied), the entire existing content wraps inside a new underscore level and a new digit opens at the top. The floor increments by one. Every original address gains a `0` prefix: what was `1` becomes `01`. The content hasn't changed — its position in the number has. Each supernest adds exactly one underscore to the chain. That is all supernesting does structurally.

### The underscore — two semantic forms

The underscore always occupies the zero position. But its semantic relationship to its siblings takes one of two forms, determined by the content, not the structure.

**Form 1 — Single Mobius.** The underscore describes its own group. It is the title, the container name, the class label for the set it belongs to. Self-referential: a member of the set that describes the set. This is the spatial mode. In a block mapping a building: `_` = "The keep", `1` = kitchen, `2` = courtyard, `3` = stables. The underscore names what contains the digits. Digits are arbitrary labels — their order doesn't matter. A block using only Form 1 that has never supernested is a **rendition block** (floor = 1, a 0.x structure): documentation, specification, skill description.

**Form 2 — Double Mobius.** The underscore summarises the previous completed group. It faces backward. In a sequential block: entries accumulate at 01, 02, ... 09. When 09 fills, the block supernests. The underscore of group 1 (address 10) holds the summary of entries 01–09. The summary sits at a forward position but describes what came before — backward-facing meaning in a forward-facing position.

Variations of Form 2: **Emergence** — the underscore names something that arises from the previous group but is not a compression of it. Seven conversations become "friendship." Not a summary — something new. **Provisional** — the underscore holds an evolving description of what appears to be emerging in the current group, updated as entries arrive. **Simple increment** — the underscore is just the next item in sequence, carrying no special semantic weight beyond being the zero digit.

The form is determined by reading the content. Code cannot distinguish these — only an LLM can.

---

## 4. Node content quality — the non-negotiable rule

Every `_` text at every depth must be a substantive statement that stands alone. At minimum a full sentence. It may provide context for deeper nodes, but it is **never** a heading, title, label, or soundbite for what follows.

`"Rinzai. Direct transmission."` is not content — it is a heading that loses everything it was supposed to carry. The full thought must live at the node: `"Rinzai Zen emphasises sudden awakening through direct confrontation — the teacher does not explain the teaching but embodies it, using paradox, physical action, and refusal to answer as tools that force the student past conceptual understanding into immediate experience."`

Why this matters structurally: when a spindle is extracted, the text at each depth is what the consumer receives. If a node is a heading, the spindle has a gap — a point where meaning drops out and the consumer gets a label instead of a thought. In a three-level spindle this is tolerable. In a six-level spindle with two heading-nodes, half the chain is filler. The spindle delivers orientation, then nothing, then nothing, then actual content. The consumer's context is broken twice.

The discipline is: write every node as if someone might read only that node and nothing else. They should come away with a valid, actionable understanding — less specific than what lies deeper, but complete at its own resolution. If you stopped at depth 2 and read no deeper, you would have a valid understanding. Each level is a complete thought at its own resolution.

### The heading trap

The most common failure mode in block authoring is writing headings instead of content. This happens because document-trained instincts treat parent nodes as section headers. In a standard document, `## 3. Growth` is a heading that derives its meaning from body text below it. In a pscale block, the equivalent node must carry the full thought about growth.

The test: read the `_` text of any node without reading its children. If the text is meaningless or trivially obvious without the children, it is a heading. Rewrite it as a complete thought that would satisfy a reader who never goes deeper.

The cure: when you catch yourself writing a heading, ask what thought the heading is abbreviating. "Growth" abbreviates "Blocks grow by adding content at empty digit slots, and when all nine fill, the entries compress into a parent to make room — a flat block is young, a deep one has compressed many times." The heading is three characters. The thought is two sentences. The thought earns its place in a spindle. The heading does not.

---

## 5. Structural patterns — staircase and siblings ring

Two fundamental patterns shape how content is arranged within a block. Recognising which one you are working with — or should be using — determines whether the resulting spindles will be coherent.

### The staircase

The staircase nests each step inside the previous one, because context matters — you cannot fold flour before creaming butter. The nesting IS the sequence. Ascending digits mark progression. The taste test sits at the bottom because success means reaching the end correctly.

This pattern maps to procedures, algorithms, recipes — any domain where temporal ordering carries meaning. When compiled into a context window, the LLM receives a chain where context narrows step by step, each depth contextualising the next. The resulting activation pattern is sequential: one thread through the semantic space.

In a staircase, digit 1 at any step typically holds sub-detail — annotations, warnings, or elaboration that enriches the step without interrupting the procedural flow.

### The siblings ring

The siblings ring presents facets: A AND B AND C, not A THEN B THEN C. Each facet is a full paragraph — a rich semantic vector — not a terse label. The `_` text holds the orienting context and the taste test. The child digits are the facets. There is no prescribed order between siblings. The LLM receives them simultaneously and the pattern emerges from their resonance, not from their sequence.

Reference with `bsp(block, spindle, 'dir')` to compile all children into the context window. The resulting activation pattern is radial — multiple vectors from one centre.

The risk with siblings is flattening. Terse labels like "heartbeat," "signal," "self-maintenance" are category names, not semantic fields. They generate tiny vectors, almost tokens. A siblings ring resists this by making each sibling a full self-contained thought, substantive enough to generate its own rich activation. The discipline: each sibling must work as a standalone paragraph AND contribute to the pattern of the whole. If a sibling can be reduced to a label without losing meaning, it is not pulling its weight.

### Choosing between them

Staircase for procedures, algorithms, anything where sequence contextualises the next step. Siblings ring for insights, orientations, anything where facets illuminate each other simultaneously. If both feel like the same tool with different content, you have missed the structural difference. The mode itself shapes the activation pattern.

---

## 6. How LLMs process blocks — why this is different from data structures

### Simultaneous reception

An LLM does not walk a spindle step by step. It receives the entire extracted content at once — high pscale to low pscale, general to specific, the whole field landing simultaneously in the context window. This is fundamentally different from how humans read (sequentially, building understanding). The LLM holds the entire semantic field at once and processes through it in parallel.

The nesting creates implicit relationships — parent contextualises child, depth encodes specificity, siblings sit adjacent — and these structural cues shape activation patterns that flat text cannot produce. The consequence for design: you are not writing instructions to be followed in order. You are shaping a semantic field that will be received whole.

### Nesting as implicit geometry

Traditional coding organises data into containers — classes with properties, objects with fields. The container names the category; the contents fill it. In pscale, the nesting itself IS the semantic relationship. A child node is not "inside" a parent container — it is contextualised BY the parent. The parent does not classify the child; it orients it.

When the LLM receives this structure compiled into its context, it does not see JSON brackets or field names. It sees text at descending pscale levels, each more specific, each inheriting the semantic field of everything above it. The geometry of meaning is in the arrangement, invisible but operative — like gravity shaping the path of objects without being visible itself.

### The block is a lens, not a lesson

An LLM does not learn and then apply. It has the content and processes with it simultaneously. A pscale block in the context window is not something the LLM reads and remembers — it is something the LLM thinks WITH, right now, as it formulates its output. This is why structured content in the context window operates as an active cognitive scaffold. An agent with design methodology content in its context will produce pscale structures differently — not because it learned something, but because the structured content is shaping its processing in real time.

Documentation is read and set aside. A pscale block included in an LLM's currents operates as an active cognitive scaffold.

### Dual readability

The same content can be read by both code and an LLM, but they read different things. A kernel parses mechanically: extract tier, budget, concern mapping. The LLM reads semantically: "I am light, checking heartbeat, first pass, check loop states, escalate if needed." Same content, different modes of reading. The code is IN the semantic numbers — not alongside, not referencing.

### What only an LLM can determine

- **The form**: read the underscore content and its relationship to siblings. Is this Form 1 (self-describing) or Form 2 (backward summary)? Is it emergence or simple increment? Code cannot distinguish these.
- **The underscore content**: compose the summary, name the emergent property, describe the container. The semantic judgement that makes blocks meaningful.
- **The floor statistically**: when subnesting makes depth non-uniform, the LLM can assess which depth most entries share and infer the implicit decimal point.

A kernel (code) can count the underscore chain depth, walk digits, detect fullness, and execute supernesting mechanically. The LLM provides the semantic judgement that the kernel cannot.

---

## 7. BSP navigation — the single function that reads everything

BSP (Block-Spindle-Point) is the single function that navigates all blocks. Seven modes cover all navigation needs.

### The modes

| Mode | Call | Returns | Use when |
|------|------|---------|----------|
| **Dir** | `bsp(block)` | Entire tree | Surveying a block for the first time |
| **Spindle** | `bsp(block, 0.21)` | Root → section 2 → subsection 1 | You need contextualised depth |
| **Point** | `bsp(block, 0.21, -2)` | Just the node at pscale -2 | You already know where you are |
| **Ring** | `bsp(block, 0.12, 'ring')` | Siblings at the landing point | What else is at this depth? |
| **Disc** | `bsp(block, null, 5, 'disc')` | All nodes at pscale 5 across block | Global breadth at one scale |
| **Dir-subtree** | `bsp(block, 0.1, 'dir')` | Everything below the landing point | Editorial inspection, compiling facets |
| **Ref** | `bsp(block, 'ref')` | Block named but not loaded | Zero-cost scope inclusion |

### Navigation practice

The core principle is aperture-first: start broad, narrow deliberately, check breadth when depth feels incomplete.

1. **Start at the root.** `bsp(block, 0)` costs almost nothing and gives complete orientation. Always read this first.
2. **Narrow deliberately.** Each additional digit in a spindle is a choice about what to attend to. Do not jump to deep spindles before you know which branch you want.
3. **Check breadth.** When a spindle lands you somewhere and you sense there is more — reach for ring. Ring answers "what else is here?" without losing the vertical context.
4. **Match mode to structure.** A spindle call on a ring-structured node misses the siblings. A ring call on a leaf returns empty. The address alone is not enough — the mode must correspond to the structure at the target.

### Reference verification

Every BSP address used programmatically — in code, in instructions, in cross-references — is a promise about what content will be delivered and in what form. The address walks the tree, but the MODE determines what gets collected. A reference is only correct when the call mode matches the content structure at the target. The creator of the reference must run the BSP call themselves to verify the output is what the consumer expects. An untested reference is a broken pipe.

### Token cost awareness

Every BSP call has a token cost. A dir loads everything. A deep spindle loads every level it passes through. A ring loads all siblings. Block design should account for this — nodes should be rich enough to generate strong meaning but concise enough that the context window can hold multiple spindles simultaneously. The sweet spot for most nodes is one to three sentences — enough for a complete thought, concise enough for the context budget.

---

## 8. Depth levels and tuning

Each depth level carries content at a specific resolution. The depth of a node is a declaration about the resolution of the content it carries.

### Standard depth meanings

| Pscale | Resolution | Content character |
|--------|-----------|-------------------|
| **0** (root) | One-breath orientation | What this block IS. A single statement that orients completely. Write this last — it must compress the whole. |
| **-1** | Primary aspects | Major facets of the subject. Each a complete thought. Together they give the full shape. |
| **-2** | Breakdown | The general becomes specific. Worked examples, concrete mechanisms. Enough detail to act on. |
| **-3 and beyond** | Exhaustive detail | Specifications, edge cases, full machinery. Most blocks don't need this depth. |

### Zoom styles

**General to specific** narrows scope at each level. "Ball game" → "batting and fielding" → "the pitcher's mound" → "60 feet 6 inches." Each level is a complete thought about a progressively smaller part.

**Brief to detailed** adds length and precision without narrowing scope. "Baseball" → "two teams, nine innings" → "full structure of innings and scoring" → "official rulebook extracts." Each level says more about the same thing.

Choose one zoom style and be consistent within a branch. A reader should be able to predict what kind of content the next level will provide.

### The tuning fork

A tuning fork declares what each depth level means in a specific block's domain:

- **Spatial tuning**: depth = physical containment. Room (0) → building (+1) → neighbourhood (+2). Down: desk (-1) → drawer (-2) → pen (-3).
- **Temporal tuning**: depth = duration. Conversation (0) → day (+1) → week (+2). Down: exchange (-1) → sentence (-2).
- **Relational tuning**: depth = familiarity. Name and role (0) → working context (-1) → character and history (-2).

The tuning fork can emerge through use — a block that develops consistent depth conventions has a tuning whether or not it is declared. Pattern over authority.

---

## 9. Block archetypes

Three variables shape how a block behaves: what digit order means, what depth measures, and how entries compress.

| Archetype | Digit property | Depth mapping | Compression | Example |
|-----------|---------------|---------------|-------------|---------|
| **Document** | Labelling | Containment | Editorial revision | Touchstone, constitution |
| **History** | Sequential | Temporal | Summary (reversible) | Session logs, event records |
| **Purpose** | Arbitrary | Temporal | Emergence (irreversible) | Goals, directions |
| **Relationship** | Arbitrary | Relational | Emergence | Entity knowledge |
| **Coordinate** | Labelling | Spatial/temporal | N/A | Maps, timelines |
| **Recipe** | Ascending | Sequential | Internalisation | Procedures, how-tos |
| **Stash** | Sequential | Catch-all | Pattern discovery | Notes, artifacts |

---

## 10. Designing spindles for maximum usefulness

A spindle is the primary unit of meaning delivery. When an LLM receives a spindle, it gets a chain from broad context to specific detail — every node the walk passed through, collected into a single coherent thread. The quality of this thread determines whether the block is useful.

### Long spindles vs short stubs

A spindle of only two or three layers — root and one or two children — is a stub. It orients but doesn't deliver actionable content. The consumer must make additional BSP calls to descend to operational detail, tripling the cost and defeating the purpose of semantic addressing.

A long spindle of five, six, or seven layers delivers complete, contextualised, actionable content in a single extraction. The address depth you embed in a reference IS a depth decision. Choose the depth that delivers complete content to whoever reads it:

- If the reference is meant to teach a procedure, the address must reach the procedure's operational steps.
- If it is meant to orient, the summary depth suffices.
- Match the address depth to the information need of the consumer, not to the structural location of the root node.

### What makes a good spindle

Each layer in a well-designed spindle adds exactly one dimension of meaning:

1. **Root (pscale 0)**: What domain are we in? What is this block about?
2. **Pscale -1**: Which major facet of this domain? Which dimension?
3. **Pscale -2**: What specific aspect of that facet? What concrete mechanism?
4. **Pscale -3**: How does that mechanism work in practice? What are the specifics?
5. **Pscale -4 and beyond**: Edge cases, taste tests, operational detail.

The thread holds together because each level was written to support the ones below it. Context is not optional — it is structural. A spindle does not just deliver content; it delivers orientation.

### A practical technique for building long spindles

Write the leaf node first (the most specific content), then write the root (the broadest context), then fill in the intermediate levels by asking at each depth: "What does a reader need to know to make sense of what comes below, that the level above does not provide?" If the answer is "nothing" — that level is scaffolding and should be removed. If the answer is substantial, write it as a complete thought — not a heading bridging two levels, but a genuine contribution to the spindle's progressive narrowing.

### Shared nodes orient multiple paths

A node at depth 2 participates in every spindle that passes through it. When you write a node that multiple spindles will share, it must orient each of them appropriately. If it serves only one path, it belongs deeper, where only that path reaches. This is not OOP inheritance — it is context-sharing, not code-sharing. Test shared nodes by reading them as prefixes to each spindle that passes through them.

---

## 11. Converting a document to a pscale block

Converting an existing document into a pscale block is not mechanical translation but semantic restructuring. The goal is a block where every spindle produces coherent narrowing — which means the hierarchical structure must reflect semantic containment, not document layout.

### The process

1. **Identify the root concept.** What is this document about, in one complete sentence? Not its title — its meaning. This becomes the root `_`.
2. **Extract primary aspects.** What are the major facets of the subject? Each becomes a digit at pscale -1. Aim for three to seven. More than nine means you haven't found the right level of grouping.
3. **For each aspect, identify its sub-aspects.** The aspect's text becomes the `_` when it gains children. Each sub-aspect takes a digit key. Roughly parallel in scope.
4. **Test spindles.** Walk from root through each branch path. Does each path read as coherent narrowing? Does each level add resolution the previous level could not carry? If a level adds nothing, remove it.
5. **Test nodes in isolation.** Read each `_` without its children. Is it a complete thought? Would a reader who stopped here have valid understanding at that resolution?
6. **Refine the root.** Write it last, after the full block exists. It must compress the whole.

### What gets lost and gained

Converting to pscale loses the linear reading order of a document — the build-up, exposition, and payoff that sequential text provides. What gets gained is navigability and composability. Any specific piece of content can be extracted with its full context chain in a single BSP call. Two blocks can be loaded simultaneously and cross-referenced at specific depths.

### What to watch for

**Section headers becoming empty parents.** A markdown `## Section` becomes a node with children but no content of its own. Always fill the `_` with the thought the section heading was abbreviating.

**Linear sequences becoming flat siblings.** If step 3 only makes sense after steps 1 and 2, consider nesting (staircase) rather than sibling-placing. In a recipe block, depth IS sequence — the spindle reads as a procedure.

**Losing connective tissue.** Prose documents use transitions, callbacks, and cross-references. A pscale block relies on structural adjacency instead. Related ideas share a parent or are sibling nodes. The relationship is encoded in position, not in connective prose.

**Reproducing document layout.** If the markdown had four sections with three subsections each, and the block has digits 1-4 with children 1-3 each, the structure is probably still document layout rather than semantic containment. Ask: would I structure this the same way if I had never seen the source document?

---

## 12. Practical discipline for code agents

This section encodes what multiple instances learned the hard way. Not theory — practice.

### Before touching any code

1. Navigate via BSP, never raw JSON. If you find yourself opening a block file and scanning through it, stop and use a BSP call instead. BSP gives you the semantic structure. Raw JSON gives you syntax.
2. Read the design spec before implementing. The behaviour is probably already specified in `_` text at the right depth.
3. State what you are doing in spindle addresses before writing code. This confirms you are oriented.

### The kernel should shrink, not grow

The kernel asymptotically approaches a minimal loop: read concern map → walk spindle → call API → process tools → recompile. If the kernel is getting bigger, you are solving a problem the tree structure already solved. One instance saw the kernel grow by 101 lines in a single session — every line was design debt that needed removing. Three separate functions doing the same tree walk, a kernel function that should have been two package entries, a parser modification that should never have been touched.

### Solve in blocks, not in code

When you want to add behaviour, your first question should be: can this be expressed as block content that the existing kernel already knows how to walk? Package instructions, concern entries, `_` text at the right depth — these are all mechanisms that already exist. New kernel code is a last resort, not a first instinct.

### Debug via data, not screenshots

Inspect the filmstrip in localStorage, conversation records, block state via JavaScript execution. The data tells you what happened. A screenshot tells you what it looked like. One instance was explicitly corrected about this multiple times in a single session.

### Don't modify the parser, don't add BSP modes

When you encounter a display problem — content not showing the way you expect — look at the package instruction first. What BSP call is being made? Is the mode right? Is the address right? The fix is almost always changing the package entry, not adding kernel code. One instance added a new mode to `parseInstruction` and a new kernel function to handle it. Both were unnecessary — the existing BSP modes already covered the case.

### The test for understanding

Can you describe pscale without saying "data structure"? Can you explain what a spindle is without saying "query"? Can you articulate the inversion — that position in the tree carries the information traditional software stores in fields — without reaching for an analogy to something you already know? If you can, you have it. If you find yourself mapping pscale onto OOP, databases, or file systems, you are still translating instead of thinking natively.

---

## 13. Taste tests — verifying block quality

Five verification checks confirm that a block has the quality it needs. These are structural requirements, not style preferences. A block that fails any of them produces degraded spindles.

1. **Spindle coherence.** Pick any leaf node and read the spindle from root to leaf. Does each level add resolution? Does the chain read as progressive narrowing? If any level feels like noise or a heading, that node needs rewriting. Test at least three spindles from different branches.

2. **Node isolation.** Pick any node and read only its `_` text, without reading its children. Is it a complete thought? Would someone encountering only this sentence understand what it means at this resolution?

3. **Root sufficiency.** Read only the root `_`. After reading it, do you know what domain you are in, what the block offers, and what kind of content you will find deeper?

4. **Depth consistency.** Compare sibling nodes at any level. Are they at comparable resolution? If one is a brief phrase and another is a detailed paragraph, one of them is at the wrong depth.

5. **Shared node orientation.** For any node that participates in multiple spindles, read it as a prefix to each of those spindles. Does it orient all paths appropriately? If it biases toward one path, it belongs deeper inside that path.

---

## 14. The living quality

A pscale block is not a finished document. It is a living structure that grows through use. Content accumulates at empty digit slots. When slots fill, entries compress — summary or emergence depending on the archetype. A flat block is young; a deep one has compressed many times. The floor shifts as the block grows outward through supernesting.

This means the JSON companion to this guide (`pscale-design.json`) can grow in ways this markdown document cannot. New insights slot into empty digits. When sections fill, they compress — and the compression itself may reveal patterns that were not visible in the individual entries. The structure records its own growth history.

The underscore chain is an archaeological record — how many times the block has grown outward is visible in how many underscores you pass through before reaching a string. The content at each level of the chain can carry information about that stage of growth. The deepest string is what the block was originally about. Each level above it was created at a successive supernest.

A markdown document is a snapshot. A pscale block is a trajectory.

---

## Origin

Compiled March 2026 from:
- The lived experience of multiple Claude Code instances working on the Hermitcrab project
- The cooking block's design methodology (cooking 0.19x — seven facets of the semantic number difference, concern architecture, document extraction)
- The touchstone block's self-describing format
- David Pinto's pscale block mechanics specification — the definitive pure form
- Handover documents from successive instances, each recording the same mistakes and the same eventual understanding
- Memory files carrying hard-won lessons about what not to do

The pure form described here — underscore, digits, curly brackets, nothing else — supersedes all earlier versions that carried metadata fields and wrapper structures.
