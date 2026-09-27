# Primer Structure Overview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every future `english-explain` structure overview use the approved background-only Primer-inspired design and natural uncolored role boundaries.

**Architecture:** Update the deterministic HTML renderer so styling and whitespace handling are enforced centrally. Update only the structure-overview instructions and output checklist in `SKILL.md`; preserve all unrelated user changes.

**Tech Stack:** Python, HTML fragments, CSS custom properties, Markdown skill instructions.

---

### Task 1: Update structure-overview instructions

**Files:**
- Modify: `SKILL.md`

- [x] Replace references to colored underlines with low-saturation background fills.
- [x] Require legend markers to reuse the sentence-span tint.
- [x] Require source whitespace between roles to remain uncolored and forbid synthetic margins or gradients.

### Task 2: Update the shared renderer

**Files:**
- Modify: `scripts/render_structure_overview.py`

- [x] Move role-segment edge whitespace outside the generated `<span>` without changing concatenated text.
- [x] Replace underline styling with 7% background tints and matching legend markers.
- [x] Add the approved heading, card, responsive legend, and relationship-tree layout.

### Task 3: Perform user-authorized mechanical validation

**Files:**
- Validate: `SKILL.md`
- Validate: `scripts/render_structure_overview.py`

- [x] Compile the Python script.
- [x] Render one fixture and confirm exact visible text, uncolored boundary spaces, background-only roles, and matching legend tints.
- [x] Run the Codex skill validator and `git diff --check`.

Behavioral subagent tests are intentionally omitted at the user's explicit request.
