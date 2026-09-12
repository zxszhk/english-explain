# Nested Clause Overview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a conditional clause-nesting overview to complex English sentence explanations.

**Architecture:** Keep the behavior in the existing `SKILL.md`. Add one trigger-and-format rule under grammar output, plus one compact example under English structure formatting; do not create scripts or change the fixed four-section response format.

**Tech Stack:** Markdown skill instructions, Codex skill validator, behavioral prompt checks.

---

### Task 1: Add and verify the structure-overview rule

**Files:**
- Modify: `SKILL.md`
- Test: behavioral runs against `SKILL.md`

- [ ] **Step 1: Record the failing baseline**

Run the existing skill against a sentence containing a main clause, a `how` object clause, a `because` reason clause, a gerund phrase, and a nested `that` clause.

Expected baseline: the response explains each structure separately but does not present one overview that maps all nesting levels.

- [ ] **Step 2: Add the minimal instruction**

After the existing grammar-output rule, add:

```markdown
- **结构总览：** 当一句包含两层以上的从句嵌套、多个从句的并列归属不清，或修饰范围容易误判时，在 `### 基本句型` 之后增加 `### 结构总览`。使用纯文本代码块，以主句为外层骨架，用方括号标出从句边界，并用缩进或连线注明“从句类型 + 句法功能／修饰对象”。简单单层从句无需绘制。结构图只呈现原句实际存在的结构；解释性的完整形式、省略来源和存在歧义的还原放在后文，不混入结构图，也不写成唯一来源。
```

Under `### 英文引用与结构片段`, add one compact example showing labels attached to their corresponding nesting level.

- [ ] **Step 3: Validate Markdown and skill metadata**

Run:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\english-explain
git diff --check
```

Expected: validator reports success and `git diff --check` produces no errors.

- [ ] **Step 4: Verify complex and simple behavior**

Run two behavioral prompts with the updated skill:

1. The complex baseline sentence must include `### 结构总览`, correctly nesting the `how`, `because`, and `that` clauses without inventing `so that`.
2. `I know that he left.` must not include `### 结构总览` because its single clause relationship is already clear.

- [ ] **Step 5: Commit the skill update**

```powershell
git add -- SKILL.md docs/superpowers/plans/2026-09-12-nested-clause-overview.md
git commit -m "feat: add nested clause structure overview"
```
